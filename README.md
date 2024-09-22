# Reading Practice

This project is a small web app prototype that generates custom stories for young students to practice their reading skills. It consists of a FastAPI backend that generates text stories and illustrations using generative AI LLMs and image models, and a Vue frontend that provides an interface for inputting story parameters and displaying the generated stories.

## Project Structure

The project is divided into two main components:

1. Backend (Python/FastAPI)
2. Frontend (Vue.js/Vite/Tailwind CSS)

### Backend

The backend is a FastAPI application that uses OpenAI's API and/or [OpenRouter's API](https://openrouter.ai) to generate stories based on user input. It's located in the `backend` directory and consists of the following key files:

- `app.py`: The main FastAPI application
- `prompts.py`: Contains the system and user prompts for the AI
- `safety_prompts.py`: Contains the system and user prompts for safety evaluation of user inputs
- `requirements.txt`: Lists the Python dependencies

### Frontend

The frontend is a Vue.js application that provides the user interface for the story generator. It's located in the `frontend` directory and uses Vite as the build tool. Key files include:

- `src/App.vue`: The main Vue component
- `src/components/InputForm.vue`: View for user input
- `src/components/StoryModal.vue`: View for displaying the generated story
- `src/components/SettingsModal.vue`: View for displaying the generated story
- `src/services/ai.js`: Utility functions for interacting with the backend

## Setup and Installation

To set up this project locally, follow these steps:

1. Clone the repository.

2. Set up the backend:
   ```
   cd backend
   python -m venv venv # Create a virtual environment
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Copy the `backend/.env.template` file to a new file called `.env`. Update the `.env` file with your API keys and other environment variables.

4. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

5. Copy the `frontend/.env.template` file to a new file called `.env`. For local development, you can keep all the default values.

## Running the Application

1. Start the backend server:
   ```
   cd backend
   source ./venv/bin/activate
   python app.py
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173` (or the URL provided by Vite).

## Usage

1. Enter the vocabulary words to include in the story.
2. Specify a main character for the story.
3. Enter a setting for where the story takes place.
4. Adjust the humor level.
5. Click "Go" to create a custom story.

Additionally, you can specify which grade level the story should be written for along with the color theme for the prototype by clicking on the Settings gear button in the lower-left.

## Customizing CSS Themes

All themes are managed by Tailwind using the [tailwindcss-themer](https://github.com/RyanClementsHax/tailwindcss-themer?tab=readme-ov-file) package.

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2024-present, Mike Creighton
