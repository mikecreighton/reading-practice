# Reading Practice Story Generator

This project is a small web app prototype that generates custom stories for young students to practice their reading and spelling skills. It consists of a Flask backend that generates text stories and illustrations using AI, and a Vue frontend that provides an interface for inputting story parameters and displaying the generated stories.

## Project Structure

The project is divided into two main components:

1. Backend (Python/Flask)
2. Frontend (Vue.js/Vite/Tailwind)

### Backend

The backend is a Flask application that uses OpenAI's API to generate stories based on user input. It's located in the `backend` directory and consists of the following key files:

- `app.py`: The main Flask application
- `prompts.py`: Contains the system and user prompts for the AI
- `requirements.txt`: Lists the Python dependencies

### Frontend

The frontend is a Vue.js application that provides the user interface for the story generator. It's located in the `frontend` directory and uses Vite as the build tool. Key files include:

- `src/App.vue`: The main Vue component
- `src/components/InputForm.vue`: Component for user input
- `src/components/StoryModal.vue`: Component for displaying the generated story

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

5. Create a `.env` file in the `frontend` directory with the following content:
   ```
   VITE_API_URL=http://localhost:8080
   ```

## Running the Application

1. Start the backend server (after activating the virtual environment):
   ```
   cd backend
   python app.py
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173` (or the URL provided by Vite).

## Usage

1. Enter the spelling words you want to practice, separated by commas.
2. Specify a main character for the story.
3. Enter a setting for the story.
4. Adjust the humor level using the slider.
5. Click "Generate Story" to create a custom story.

## Customizing CSS Themes

All themes are managed by Tailwind using the [tailwindcss-themer](https://github.com/RyanClementsHax/tailwindcss-themer?tab=readme-ov-file) package.

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (c) 2024-present, Mike Creighton