import os
import time
import json
from typing import List, Tuple
from openai import AsyncOpenAI, RateLimitError
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger as fastapi_logger
import logging
from pydantic import BaseModel
from prompts import (
    USER_PROMPT,
    SYSTEM_PROMPT,
    ILLUSTRATION_SYSTEM_PROMPT,
    ILLUSTRATION_USER_PROMPT,
)
from safety_prompts import (
    SYSTEM_PROMPT as SAFETY_SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE as SAFETY_USER_PROMPT_TEMPLATE,
)
import httpx
import asyncio

# -----------------------------------------
#
# Initialization
#
# -----------------------------------------


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit=8, window=60, exempt_routes: List[Tuple[str, str]] = []):
        super().__init__(app)
        self.limit = limit  # Number of requests allowed
        self.window = window  # Time window in seconds
        self.ip_cache = {}
        self.exempt_routes = set(exempt_routes)

    async def dispatch(self, request: Request, call_next):
        # Check if the current route is exempt
        current_route = (request.url.path, request.method)
        if current_route in self.exempt_routes:
            return await call_next(request)

        ip = request.client.host
        current_time = time.time()

        if ip in self.ip_cache:
            last_reset, count = self.ip_cache[ip]
            if current_time - last_reset > self.window:
                # Reset if the window has passed
                self.ip_cache[ip] = (current_time, 1)
            elif count >= self.limit:
                # Return a JSONResponse for rate limit exceeded
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded. Please try again later."},
                )
            else:
                self.ip_cache[ip] = (last_reset, count + 1)
        else:
            self.ip_cache[ip] = (current_time, 1)

        response = await call_next(request)
        return response


load_dotenv(override=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    """
    When running with gunicorn the log handlers get suppressed instead of
    passed along to the container manager. This forces the gunicorn handlers
    to be used throughout the project.
    """

    gunicorn_logger = logging.getLogger("gunicorn")

    root_logger = logging.getLogger()
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")

    # Use gunicorn error handlers for root, uvicorn, and fastapi loggers
    root_logger.handlers = gunicorn_error_logger.handlers
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers

    # Pass on logging levels for root, uvicorn, and fastapi loggers
    root_logger.setLevel(logging.INFO)
    uvicorn_access_logger.setLevel(logging.INFO)
    fastapi_logger.setLevel(logging.INFO)


# AI configuration
AI_TEXT_PROVIDER = os.getenv("AI_TEXT_PROVIDER", "openai")
AI_SAFETY_MODEL = os.getenv("AI_SAFETY_MODEL", "gpt-4o-mini")
AI_IMAGE_PROVIDER = os.getenv("AI_IMAGE_PROVIDER", "none")

if AI_TEXT_PROVIDER == "openai":
    AI_TEXT_API_KEY = os.getenv("OPENAI_API_KEY")
    AI_TEXT_BASE_URL = "https://api.openai.com/v1"
    DEFAULT_TEXT_MODEL = "gpt-4o"
elif AI_TEXT_PROVIDER == "openrouter":
    AI_TEXT_API_KEY = os.getenv("OPENROUTER_API_KEY")
    AI_TEXT_BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_TEXT_MODEL = "anthropic/claude-3.5-sonnet"

text_client = AsyncOpenAI(api_key=AI_TEXT_API_KEY, base_url=AI_TEXT_BASE_URL)

AI_TEXT_MODEL = os.getenv("AI_TEXT_MODEL", DEFAULT_TEXT_MODEL)
TEMPERATURE = 0.8
MAX_TOKENS = 256

# Instantiate the FastAPI app
app = FastAPI()

# Add the rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    limit=5,
    window=60,
    exempt_routes=[("/", "GET"), ("/image_provider_available", "GET")],
)

# CORS configuration
if os.getenv("SERVER_ENV") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[os.getenv("FRONTEND_ORIGIN")],
        allow_credentials=True,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["*"],
    )

# -----------------------------------------
#
# Helper functions
#
# -----------------------------------------


def construct_user_prompt(words, subject, setting, humor, grade):
    """
    Construct the user prompt for the story generator using the prompt
    template in prompts.py.
    """
    user_prompt = (
        USER_PROMPT.replace("{{words}}", words)
        .replace("{{subject}}", subject)
        .replace("{{setting}}", setting)
        .replace("{{humor}}", humor)
        .replace("{{grade}}", grade)
    )
    # Add a timestamp to prevent caching when using OpenRouter
    if AI_TEXT_PROVIDER == "openrouter":
        user_prompt += f"\n\n[IGNORE THIS: Timestamp: {time.time()}]"
    return user_prompt


def construct_illustration_user_prompt(story, grade):
    """
    Construct the user prompt for the illustration generator using the prompt
    template in prompts.py.
    """
    return ILLUSTRATION_USER_PROMPT.replace("{{story}}", story).replace("{{grade}}", grade)


# -----------------------------------------
#
# Pydantic models
#
# -----------------------------------------


class StoryRequest(BaseModel):
    words: str
    subject: str
    setting: str
    humor: str
    grade: str


class IllustrationRequest(BaseModel):
    story: str
    grade: str
    aspect_ratio: str


# -----------------------------------------
#
# Routes
#
# -----------------------------------------


@app.get("/image_provider_available")
async def image_provider_available(request: Request):
    """
    Lets the client know if the image provider is available
    so that it knows whether or not to attempt to generate an image.
    """
    return {"message": AI_IMAGE_PROVIDER != "none"}


@app.post("/generate_story")
async def generate_story(request: StoryRequest):
    """
    Generate a story with integrated content safety check.
    """

    logging.info(f"\n------------\nNew story request: {request}")

    # Perform safety check
    safety_user_prompt = (
        SAFETY_USER_PROMPT_TEMPLATE.replace("{{words}}", request.words)
        .replace("{{grade}}", request.grade)
        .replace("{{subject}}", request.subject)
        .replace("{{setting}}", request.setting)
    )

    # Add a timestamp to prevent caching when using OpenRouter
    if AI_TEXT_PROVIDER == "openrouter":
        safety_user_prompt += f"\n\n[IGNORE THIS: Timestamp: {time.time()}]"

    try:
        safety_response = await text_client.chat.completions.create(
            model=AI_SAFETY_MODEL,
            messages=[
                {"role": "system", "content": SAFETY_SYSTEM_PROMPT},
                {"role": "user", "content": safety_user_prompt},
            ],
            temperature=0,
            max_tokens=1024,
        )
    except RateLimitError:
        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded. Please try again later."},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)},
        )

    safety_content = safety_response.choices[0].message.content

    # Need to make sure that we've got something that looks like JSON.
    try:
        if "```json" in safety_content:
            json_part = safety_content.split("```json")[1].split("```")[0]
            safety_result = json.loads(json_part)
        else:
            safety_result = json.loads(safety_content)
        safe_value = safety_result.get("safe", False)
        appropriate_value = safety_result.get("appropriate", False)
        is_safe = appropriate_value and safe_value
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to parse safety check response"},
        )

    if not is_safe:
        return {
            "safe": False,
            "story": None,
            "reason": "unsafe" if not safe_value else "inappropriate",
            "error": "Looks like you might have tried to tell a story with words or concepts that are not appropriate for a children's story. Please go back and try again.",
        }

    # Generate story
    user_prompt = construct_user_prompt(
        request.words, request.subject, request.setting, request.humor, request.grade
    )

    try:
        response = await text_client.chat.completions.create(
            model=AI_TEXT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    except RateLimitError:
        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded. Please try again later."},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)},
        )

    story = response.choices[0].message.content

    return {"safe": True, "story": story}


@app.post("/generate_illustration")
async def generate_illustration(request: IllustrationRequest):
    """
    Generate an illustration for a given story.
    """

    if AI_IMAGE_PROVIDER == "none":
        return JSONResponse(
            status_code=400,
            content={"message": "Image provider is not available."},
        )

    if AI_IMAGE_PROVIDER == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            return JSONResponse(
                status_code=400,
                content={"message": "No OPENAI_API_KEY environment variable set."},
            )

    elif AI_IMAGE_PROVIDER == "bfl":
        if not os.getenv("BFL_API_KEY"):
            return JSONResponse(
                status_code=400,
                content={"message": "No BFL_API_KEY environment variable set."},
            )

    start = time.time()

    user_prompt = construct_illustration_user_prompt(request.story, request.grade)
    AI_ILLUSTRATION_TEXT_MODEL = os.getenv(
        "AI_ILLUSTRATION_TEXT_MODEL", "anthropic/claude-3.5-sonnet"
    )

    try:
        response = await text_client.chat.completions.create(
            model=AI_ILLUSTRATION_TEXT_MODEL,
            messages=[
                {"role": "system", "content": ILLUSTRATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    except RateLimitError:
        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded. Please try again later."},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)},
        )

    image_gen_prompt = response.choices[0].message.content

    if AI_IMAGE_PROVIDER == "openai":

        image_gen_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        if request.aspect_ratio == "square":
            size = "1024x1024"
        elif request.aspect_ratio == "landscape":
            size = "1792x1024"
        else:
            size = "1024x1024"

        try:
            image_gen_response = await image_gen_client.images.generate(
                model="dall-e-3",
                prompt=image_gen_prompt,
                size=size,
                quality="standard",
                n=1,
                response_format="b64_json",
            )
        except RateLimitError:
            return JSONResponse(
                status_code=429,
                content={"message": "Rate limit exceeded. Please try again later."},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": str(e)},
            )

        image_gen_response_b64 = image_gen_response.data[0].b64_json

        end = time.time()
        logging.info(f"/generate_illustration - Time elapsed: {end - start}")

        return {"image": image_gen_response_b64, "type": "b64"}

    elif AI_IMAGE_PROVIDER == "bfl":
        logging.info(f"Generating image with BFL")
        request_url = "https://api.bfl.ml/v1/flux-pro-1.1"

        w = 1024
        h = 1024
        if request.aspect_ratio == "landscape":
            w = 1312
            h = 736

        headers = {"Content-Type": "application/json", "X-Key": os.getenv("BFL_API_KEY")}

        data = {
            "prompt": image_gen_prompt,
            "width": w,
            "height": h,
            "prompt_upsampling": False,
            "safety_tolerance": 1,
        }

        async with httpx.AsyncClient() as client:
            try:
                # Initial request to start the job
                response = await client.post(request_url, json=data, headers=headers)
                response.raise_for_status()
                job_id = response.json()["id"]
                logging.info(f"Job ID: {job_id}")
                # Polling for the result
                result_url = f"https://api.bfl.ml/v1/get_result?id={job_id}"
                max_attempts = 30  # Adjust as needed
                for _ in range(max_attempts):
                    logging.info(f"Polling for result: {result_url}")

                    result_response = await client.get(result_url, headers=headers)
                    result_response.raise_for_status()
                    result_data = result_response.json()

                    if result_data["status"] == "Ready":
                        image_url = result_data["result"]["sample"]
                        end = time.time()
                        logging.info(f"/generate_illustration - Time elapsed: {end - start}")
                        return {"image": image_url, "type": "url"}
                    elif result_data["status"] == "failed":
                        raise Exception("Image generation failed")

                    await asyncio.sleep(1)  # Wait for 1 second before polling again

                raise Exception("Timeout waiting for image generation")

            except httpx.HTTPStatusError as e:
                return JSONResponse(
                    status_code=e.response.status_code,
                    content={"message": f"HTTP error occurred: {str(e)}"},
                )
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"message": str(e)},
                )


# Add this new route handler near the other route definitions
@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve a blank page for the root route.
    """
    return """
    <html>
        <head>
            <title>Reading Practice Backend</title>
        </head>
        <body>
        </body>
    </html>
    """


# -----------------------------------------
#
# Server startup
#
# -----------------------------------------

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8080))
    reload = os.getenv("SERVER_ENV") != "production"

    uvicorn.run("app:app", host=host, port=port, reload=reload)
