import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from prompts import USER_PROMPT, SYSTEM_PROMPT, ILLUSTRATION_SYSTEM_PROMPT, ILLUSTRATION_USER_PROMPT
from safety_prompts import SYSTEM_PROMPT as SAFETY_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE as SAFETY_USER_PROMPT_TEMPLATE
import json

# -----------------------------------------
#
# Initialization
#
# -----------------------------------------

load_dotenv(override=True)

# AI configuration
AI_TEXT_PROVIDER = os.getenv("AI_TEXT_PROVIDER", "openai")
AI_SAFETY_MODEL = os.getenv("AI_SAFETY_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

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


class UnsafeStoryException(Exception):
    def __init__(self, name: str):
        self.name = name


# -----------------------------------------
#
# Routes
#
# -----------------------------------------


@app.exception_handler(UnsafeStoryException)
async def unsafe_story_exception_handler(request: Request, exc: UnsafeStoryException):
    return JSONResponse(
        status_code=400,
        content={
            "safe": False,
            "story": None,
            "error": "Looks like you might have tried to tell a story with words or concepts that are not appropriate for a children's story. Please go back and try again.",
        },
    )


@app.post("/generate_story")
async def generate_story(request: StoryRequest):
    """
    Generate a story with integrated safety check.
    """
    start = time.time()

    # Perform safety check
    safety_user_prompt = (
        SAFETY_USER_PROMPT_TEMPLATE.replace("{{words}}", request.words)
        .replace("{{grade}}", request.grade)
        .replace("{{subject}}", request.subject)
        .replace("{{setting}}", request.setting)
    )
    safety_response = await text_client.chat.completions.create(
        model=AI_SAFETY_MODEL,
        messages=[
            {"role": "system", "content": SAFETY_SYSTEM_PROMPT},
            {"role": "user", "content": safety_user_prompt},
        ],
        temperature=0,
        max_tokens=256,
    )

    safety_content = safety_response.choices[0].message.content

    if "```json" in safety_content:
        json_part = safety_content.split("```json")[1].split("```")[0]
        safety_result = json.loads(json_part)
    else:
        safety_result = json.loads(safety_content)
    safe_value = safety_result.get("safe", False)
    appropriate_value = safety_result.get("appropriate", False)
    is_safe = appropriate_value and safe_value

    if not is_safe:
        if appropriate_value == False:
            raise UnsafeStoryException("inappropriate")
        else:
            raise UnsafeStoryException("unsafe")

    # Generate story
    user_prompt = construct_user_prompt(request.words, request.subject, request.setting, request.humor, request.grade)

    print("-----------------------------------------")
    print("Story system prompt:")
    print(SYSTEM_PROMPT)
    print(" ")
    print("Story user prompt:")
    print(user_prompt)
    print("-----------------------------------------")

    response = await text_client.chat.completions.create(
        model=AI_TEXT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    story = response.choices[0].message.content

    end = time.time()
    print("/generate_story - Time elapsed: ", end - start)

    return {"safe": True, "story": story}


@app.get("/openai_available")
async def openai_available():
    return {"message": bool(os.getenv("OPENAI_API_KEY"))}


@app.post("/generate_illustration")
async def generate_illustration(request: IllustrationRequest):
    """
    Generate an illustration for a given story.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=400, detail="No OPENAI_API_KEY environment variable set.")

    start = time.time()

    user_prompt = construct_illustration_user_prompt(request.story, request.grade)
    AI_ILLUSTRATION_TEXT_MODEL = os.getenv("AI_ILLUSTRATION_TEXT_MODEL", "anthropic/claude-3.5-sonnet")

    print("-----------------------------------------")
    print("Illustration model: ", AI_ILLUSTRATION_TEXT_MODEL)
    print("Illustration system prompt:")
    print(ILLUSTRATION_SYSTEM_PROMPT)
    print(" ")
    print("Illustration user prompt:")
    print(user_prompt)
    print("-----------------------------------------")

    response = await text_client.chat.completions.create(
        model=AI_ILLUSTRATION_TEXT_MODEL,
        messages=[
            {"role": "system", "content": ILLUSTRATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    image_gen_prompt = response.choices[0].message.content

    print("-----------------------------------------")
    print("Generated illustration response prompt for DALL-E 3:")
    print(image_gen_prompt)
    print("-----------------------------------------")

    image_gen_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    image_gen_response = await image_gen_client.images.generate(
        model="dall-e-3",
        prompt=image_gen_prompt,
        size="1792x1024",
        quality="standard",
        n=1,
        response_format="b64_json",
    )

    image_gen_response_b64 = image_gen_response.data[0].b64_json

    end = time.time()
    print("/generate_illustration - Time elapsed: ", end - start)

    return {"image": image_gen_response_b64}


# -----------------------------------------
#
# Server startup
#
# -----------------------------------------

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    reload = os.getenv("SERVER_ENV") != "production"

    uvicorn.run("app:app", host=host, port=port, reload=reload)
