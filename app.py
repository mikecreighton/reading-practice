import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response, render_template, Response

load_dotenv()

# initialize openai with my key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_url_path='', static_folder='./static')

SYSTEM_PROMPT = """Act as a professional elementary school teacher who excels in teaching basic Math and English to students. You're excellent at coming up with creative and engaging homework assignments that require minimal supervision and less than 15 minutes to complete. Your job is to take a list of spelling words that a student needs to practice, take a subject and setting provided by the student, and create a short two-paragraph story that incorporates each of the spelling words and the student's suggested subject and setting for the story. The reading level for the story should be appropriate for a 2nd grade student just entering 2nd grade.
    
# Your Inputs

You will be provided with the inputs in the following format:

- Spelling words: [comma-separated list of words]
- Subject: [subject]
- Setting: [setting]

# Examples 

Here are examples of good stories for 2nd grade reading level for a student just entering 2nd grade:

**Example 1**

The sun is hot.
It is too hot for the pig.
The pig wants to be cool.
It sees some mud.
Slosh! Slosh! Slosh!
The mud feels good.
The mud is not hot.
Roll, pig, roll!

**Example 2**

Kit is little.
But Kit has a very big dog.
So Kit has a very big room.
The room has one big bed.
And it has one little bed.
The room has one big toy box.
And it has one little toy box.
Kit is little.
But Kit has a very big dog.
Kit's very big room has a very little room for Kit!

**Example 3**

Rays are big fish in the sea.
They flap their two fins to swim.
Their fins go up and down.
They swim very fast.
Rays can flap right out of the water!
Rays open their mouths when they swim.
Their mouths are long.
Small fish go right in.
So rays eat while they swim.

**Example 4**

Jen is with her mom.
They are at a pet shop.
Jen can get a pet.
She can pick the pet she likes.
Jen looks and looks.
The dogs bark too much.
The cats sleep too much.
The birds bite too much.
The fish just swim.
"A fish is best," says Jen.

# Your Output

You will generate only a story similar to the examples above, with no additional commentary or text.
"""

USER_PROMPT = """Write me a two paragraph story using the following inputs:

Spelling words: {{words}}

Subject: {{subject}}

Setting: {{setting}}

Please note, the story must be written for a student *just* entering 2nd grade, who is 7 years old. The reading level should be appropriate for this age group.
"""

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/stream', methods=['POST'])
def stream():
    def process_stream(words, subject, setting):
        user_prompt = USER_PROMPT.replace('{{words}}', words).replace('{{subject}}', subject).replace('{{setting}}', setting)

        response = openai.ChatCompletion.create(
            model='gpt-4',
            max_tokens=1024,
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
            temperature=0.8,
            stream=True)
        for line in response:
            chunk = line['choices'][0].get('delta', {}).get('content', '')
            if chunk:
                yield chunk
    
    # get the variables from POST request coming from a json fetch request
    words = request.json['words']
    subject = request.json['subject']
    setting = request.json['setting']
    
    print("--------- New request ---------")
    print(words, subject, setting)
    
    return Response(process_stream(words, subject, setting), mimetype='text/event-stream')



@app.route('/generate', methods=['POST'])
def generate():
    # get the variables from POST request coming from a json fetch request
    words = request.json['words']
    subject = request.json['subject']
    setting = request.json['setting']

    user_prompt = USER_PROMPT.replace('{{words}}', words).replace('{{subject}}', subject).replace('{{setting}}', setting)

    response = openai.ChatCompletion.create(
        model='gpt-4',
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content": user_prompt
            },
        ])
    
    llm_response_content = response.choices[0]['message']['content']

    print(llm_response_content)

    # response will have a <story></story> tag, so we need to split on <story> and </story> and get what's in between.
    # sometimes the response will have two <story> tags, and we need the content that's in the last pair.
    story = llm_response_content.split('<story>')[1].split('</story>')[0]
    story_object = {
        "story": story
    }
    return jsonify(story_object)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)