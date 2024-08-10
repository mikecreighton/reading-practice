import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
from prompts import USER_PROMPT, SYSTEM_PROMPT, ILLUSTRATION_SYSTEM_PROMPT, ILLUSTRATION_USER_PROMPT

# -----------------------------------------
#
# Initialization
#
# -----------------------------------------

load_dotenv(override=True)

# First, we'll figure out which API service to use for text generation
AI_TEXT_PROVIDER = os.getenv("AI_TEXT_PROVIDER", "openai")

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
app = Flask(__name__, static_url_path='', static_folder='./static')

# Allow CORS for all origins if FLASK_ENV is "development"
if os.getenv("FLASK_ENV") == "development":
    CORS(app, resources={r"/*": {"origins": "*"}})
else:
    CORS(app, resources={r"/*": {
        "origins": [os.getenv("FRONTEND_ORIGIN")],
        "methods": ["POST", "OPTIONS"],
    }})

# -----------------------------------------
#
# Helper functions
#
# -----------------------------------------

def construct_user_prompt(words, subject, setting, humor):
    user_prompt = USER_PROMPT.replace('{{words}}', words).replace('{{subject}}', subject).replace('{{setting}}', setting).replace('{{humor}}', humor)
    # Add a timestamp to prevent caching when using OpenRouter
    if AI_TEXT_PROVIDER == "openrouter":
        user_prompt += f"\n\n[IGNORE THIS: Timestamp: {time.time()}]"
    return user_prompt

def construct_illustration_user_prompt(story):
    user_prompt = ILLUSTRATION_USER_PROMPT.replace('{{story}}', story)
    return user_prompt
# -----------------------------------------
#
# HELPERS
#
# -----------------------------------------

# A little helper logger in case you're having trouble with CORS origins.
# @app.before_request
# def log_request_info():
#     if os.getenv("FLASK_ENV") != "development":
#         print('Headers: %s', request.headers)
#         print('Origin: %s', request.headers.get('Origin'))


# -----------------------------------------
#
# Routes
#
# -----------------------------------------

@app.route('/')
def home():
    """

    Serve the homepage

    """
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    """

    Serve static files

    """
    return app.send_static_file(path)

@app.route('/stream', methods=['POST'])
def stream():
    """

    Used for a _streaming_ request to generate a story.

    """
    def process_stream(user_prompt):
        try:
            stream = client.chat.completions.create(model=AI_TEXT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role":"user",
                        "content": user_prompt
                    },
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield content
        except Exception as e:
            print(f"Error during streaming: {e}")
            yield f"Error: {e}"
    
    words = request.json['words']
    subject = request.json['subject']
    setting = request.json['setting']
    humor = request.json['humor']
    user_prompt = construct_user_prompt(words, subject, setting, humor)
    
    return Response(process_stream(user_prompt), mimetype='text/event-stream')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    """

    Used for a non-streaming request to generate a story.

    """
    # start a timer to evaluate how long this request takes
    start = time.time()

    words = request.json['words']
    subject = request.json['subject']
    setting = request.json['setting']
    humor = request.json['humor']

    user_prompt = construct_user_prompt(words, subject, setting, humor)

    print("-----------------------------------------")
    print("Story model: ", AI_TEXT_MODEL)
    print("Story system prompt:")
    print(SYSTEM_PROMPT)
    print(" ")
    print("Story user prompt:")
    print(user_prompt)
    print("-----------------------------------------")

    response = text_client.chat.completions.create(model=AI_TEXT_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content": user_prompt
            },
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    llm_response_content = response.choices[0].message.content

    end = time.time()
    print("/generate_story - Time elapsed: ", end - start)

    story_object = {
        "story": llm_response_content
    }
    return jsonify(story_object)

@app.route('/openai_available', methods=['GET'])
def openai_available():
    if os.getenv("OPENAI_API_KEY"):
        return jsonify({"message": True})
    else:
        return jsonify({"message": False})


@app.route('/generate_illustration', methods=['POST'])
def generate_illustration():
    """

    Used for a non-streaming request to generate an illustration.

    """
    # Only do this if the OPENAI_API_KEY environment variable is set
    if os.getenv("OPENAI_API_KEY"):

        # start a timer to evaluate how long this request takes
        start = time.time()

        story = request.json['story']
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

        response = text_client.chat.completions.create(model=AI_ILLUSTRATION_TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": ILLUSTRATION_SYSTEM_PROMPT
                },
                {
                    "role":"user",
                    "content": user_prompt
                },
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

        iamge_object = {
            "image": image_gen_response_b64
        }
        return jsonify(iamge_object)
    else:
        return jsonify({"error": "No OPENAI_API_KEY environment variable set."})

# Determine if we should use debug based on environment.
# We'll default to debug for anything that isn't "production".
if os.getenv("FLASK_ENV") == "production":
    debug = False
else:
    debug = True

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port=8080)