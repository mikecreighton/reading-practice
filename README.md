# Reading Practice

Simple web app that leverages generative AI for writing simple stories for reading practice.

## Getting started

1. Go into the `server` folder.
2. Create a virtual Python environment ([link](https://docs.python.org/3/library/venv.html)).
3. Activate your virtual Python environment.
4. Install Python dependencies:

```
pip install -r requirements.txt
```

5. Duplicate the `.env.template` and rename to `.env`.

```
cp .env.template .env
```

6. Add your OpenAI API key to the `.env` file.
7. Start the server:

```
python app.py
```

8. Visit the local website: [http://127.0.0.1:5555](http://127.0.0.1:5555)