import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import time
from prompts import USER_PROMPT, SYSTEM_PROMPT

# -----------------------------------------
#
# Initialization
#
# -----------------------------------------

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

TEMPERATURE = 0.6
MAX_TOKENS = 512
LLM = "anthropic/claude-3.5-sonnet"

app = Flask(__name__, static_url_path='', static_folder='./static')
CORS(app)

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stream', methods=['POST'])
def stream():
    """

    Used for a streaming request to generate a story.

    """

    print("--------- New /stream request ---------")

    def process_stream(user_prompt):
        stream = client.chat.completions.create(model=LLM,
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

    response = client.chat.completions.create(model=LLM,
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)