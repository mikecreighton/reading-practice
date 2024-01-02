# Reading Practice

Simple web app that leverages generative AI for writing simple stories for reading practice. The front-end is built with React, and the back-end is built with python and Flask. It makes use of the OpenAI API, specifically the GPT-4 model.

This is hard-coded for a 2nd grade reading level, but if you review the prompts in `/server/prompts.py`, you'll see that it's pretty easy to change as needed. The prompts haven't been rigorously tested as of this writing, but they're pretty good for the most part.

## Getting started

### The Back-end Server

1. In your favorite terminal, navigate to the `server` folder.
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

8. Visit the local website: [http://localhost:5555](http://localhost:5555)

### The Front-end App

The app is a very simple React app, written by someone who knows nothing about React. Here's how you get started with running it locally:

1. In your favorite terminal, navigate to the `client` folder.
2. Type `npm install` or `yarn install` to install all dependencies.
3. Copy the `.env.template` file to a new file called `.env`.

```
cp .env.template .env
```

4. In that `.env` file, replace the URL value of `REACT_APP_API_URL` for the back-end API as needed. By default, when you run the back-end server locally, it will be served at `http://localhost:5555`.
5. Type `npm run start` or `yarn start` to run the React app locally. Be sure that the back-end API server is running as well.

Please note that `node-sass` is one of the dependencies for the app. I had issues getting this to install successfully when using `npm`, so you may want to use yarn. This is why you don't see a `package-lock.json` file in this repo.