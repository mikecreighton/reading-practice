import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time
from prompts import USER_PROMPT, SYSTEM_PROMPT

# -----------------------------------------
#
# Initialization
#
# -----------------------------------------

load_dotenv(override=True)

api_key = os.getenv("AI_API_KEY")
ai_provider = os.getenv("AI_PROVIDER", "openai")
default_model = "gpt-4o"

if ai_provider == "openai":
    client = OpenAI(api_key=api_key)
elif ai_provider == "openrouter":
    default_model = "anthropic/claude-3.5-sonnet"
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

ai_model = os.getenv("AI_MODEL", default_model)
TEMPERATURE = 0.8
MAX_TOKENS = 100

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
    return user_prompt

# -----------------------------------------
#
# Routes
#
# -----------------------------------------
@app.before_request
def log_request_info():
    print('Headers: %s', request.headers)
    print('Origin: %s', request.headers.get('Origin'))

@app.route('/')
def home():
    return app.send_static_file('index.html')

# Serve static files
@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

@app.route('/stream', methods=['POST'])
def stream():
    """

    Used for a streaming request to generate a story.

    """

    print("--------- New /stream request ---------")

    def process_stream(user_prompt):
        try:
            stream = client.chat.completions.create(model=ai_model,
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

@app.route('/generate', methods=['POST'])
def generate():
    """

    Used for a non-streaming request to generate a story.

    """

    print("--------- New /generate request ---------")

    # start a timer to evaluate how long this request takes
    start = time.time()

    words = request.json['words']
    subject = request.json['subject']
    setting = request.json['setting']
    humor = request.json['humor']

    user_prompt = construct_user_prompt(words, subject, setting, humor)
    # Append a timestamp to the end of the message
    # user_prompt += f"\n\n[IGNORE THIS: Timestamp: {time.time()}]"

    response = client.chat.completions.create(model=ai_model,
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
    print("/generate - Time elapsed: ", end - start)

    story_object = {
        "story": llm_response_content
    }
    return jsonify(story_object)

# Determine if we should use debug based on environment
if os.getenv("FLASK_ENV") == "development":
    debug = True
else:
    debug = False

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port=8080)