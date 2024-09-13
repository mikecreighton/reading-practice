import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
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

# First, we'll figure out which API service to use for text generation
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

text_client = OpenAI(api_key=AI_TEXT_API_KEY, base_url=AI_TEXT_BASE_URL)

AI_TEXT_MODEL = os.getenv("AI_TEXT_MODEL", DEFAULT_TEXT_MODEL)
TEMPERATURE = 0.8
MAX_TOKENS = 256

# Instantiate the Flask app
app = Flask(__name__, static_url_path="", static_folder="./static")

# Allow CORS for all origins if FLASK_ENV is "development"
if os.getenv("FLASK_ENV") == "development":
    CORS(app, resources={r"/*": {"origins": "*"}})
else:
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [os.getenv("FRONTEND_ORIGIN")],
                "methods": ["POST", "OPTIONS"],
            }
        },
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


def construct_illustration_user_prompt(story):
    user_prompt = ILLUSTRATION_USER_PROMPT.replace("{{story}}", story)
    return user_prompt


# -----------------------------------------
#
# HELPERS
#
# -----------------------------------------


# A little helper logger in case you're having trouble with CORS origins.
@app.before_request
def log_request_info():
    if os.getenv("FLASK_ENV") != "development":
        print("Headers: %s", request.headers)
        print("Origin: %s", request.headers.get("Origin"))


# -----------------------------------------
#
# Routes
#
# -----------------------------------------


@app.route("/")
def home():
    """

    Serve the homepage

    """
    return app.send_static_file("index.html")


@app.route("/<path:path>")
def serve_static(path):
    """

    Serve static files

    """
    return app.send_static_file(path)


@app.route("/generate_story", methods=["POST"])
def generate_story():
    """
    Used for a non-streaming request to generate a story with integrated safety check.
    """
    start = time.time()

    words = request.json["words"]
    subject = request.json["subject"]
    setting = request.json["setting"]
    humor = request.json["humor"]
    grade = request.json["grade"]

    # Perform safety check
    safety_user_prompt = (
        SAFETY_USER_PROMPT_TEMPLATE.replace("{{words}}", words)
        .replace("{{grade}}", grade)
        .replace("{{subject}}", subject)
        .replace("{{setting}}", setting)
    )
    safety_response = text_client.chat.completions.create(
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

    is_safe = safety_result.get("appropriate", False) and safety_result.get("safe", False)

    if not is_safe:
        return jsonify(
            {
                "safe": False,
                "story": None,
                "error": "Looks like you might have tried to tell a story with words or concepts that are not appropriate for a children's story. Please go back and try again.",
            }
        )

    # Generate story
    user_prompt = construct_user_prompt(words, subject, setting, humor, grade)

    print("-----------------------------------------")
    print("Story system prompt:")
    print(SYSTEM_PROMPT)
    print(" ")
    print("Story user prompt:")
    print(user_prompt)
    print("-----------------------------------------")

    response = text_client.chat.completions.create(
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

    return jsonify({"safe": True, "story": story})


@app.route("/openai_available", methods=["GET"])
def openai_available():
    if os.getenv("OPENAI_API_KEY"):
        return jsonify({"message": True})
    else:
        return jsonify({"message": False})


@app.route("/generate_illustration", methods=["POST"])
def generate_illustration():
    """

    Used for a non-streaming request to generate an illustration.

    """
    # Only do this if the OPENAI_API_KEY environment variable is set
    if os.getenv("OPENAI_API_KEY"):

        # start a timer to evaluate how long this request takes
        start = time.time()

        story = request.json["story"]
        user_prompt = construct_illustration_user_prompt(story)
        # AI_ILLUSTRATION_TEXT_MODEL = os.getenv("AI_ILLUSTRATION_TEXT_MODEL", "meta-llama/llama-3.1-70b-instruct")
        AI_ILLUSTRATION_TEXT_MODEL = os.getenv("AI_ILLUSTRATION_TEXT_MODEL", "anthropic/claude-3.5-sonnet")

        print("-----------------------------------------")
        print("Illustration model: ", AI_ILLUSTRATION_TEXT_MODEL)
        print("Illustration system prompt:")
        print(ILLUSTRATION_SYSTEM_PROMPT)
        print(" ")
        print("Illustration user prompt:")
        print(user_prompt)
        print("-----------------------------------------")

        response = text_client.chat.completions.create(
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

        image_gen_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        image_gen_response = image_gen_client.images.generate(
            model="dall-e-3",
            prompt=image_gen_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json",
        )

        image_gen_response_b64 = image_gen_response.data[0].b64_json

        end = time.time()
        print("/generate_illustration - Time elapsed: ", end - start)

        iamge_object = {"image": image_gen_response_b64}
        return jsonify(iamge_object)
    else:
        return jsonify({"error": "No OPENAI_API_KEY environment variable set."})


# Determine if we should use debug based on environment.
# We'll default to debug for anything that isn't "production".
if os.getenv("FLASK_ENV") == "production":
    debug = False
else:
    debug = True

if __name__ == "__main__":
    app.run(debug=debug, host="0.0.0.0", port=8080)
