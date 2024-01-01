# Reading Practice

Simple web app that leverages generative AI for writing simple stories for reading practice.

## Getting started

1. Create a virtual Python environment ([link](https://docs.python.org/3/library/venv.html)).
2. Activate your virtual Python environment.
3. Install Python dependencies:

```
pip install -r requirements.txt
```

4. Duplicate the `.env.template` and rename to `.env`.

```
cp .env.template .env
```

5. Add your OpenAI API key to the `.env` file.
6. Start the server:

```
python app.py
```

7. Visit the local website: [http://127.0.0.1:5555](http://127.0.0.1:5555)