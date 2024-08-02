# Reading Practice Story Generator

This project is a web application that generates custom stories for elementary school students to practice their reading and spelling skills. It consists of a Flask backend that generates stories using AI, and a Vue.js frontend that provides a user-friendly interface for inputting story parameters and displaying the generated stories.

## Project Structure

The project is divided into two main components:

1. Backend (Python/Flask)
2. Frontend (Vue.js)

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

1. Clone the repository:
   ```
   git clone <repository-url>
   cd reading-practice-story-generator
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the `backend` directory with the following content:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   FLASK_ENV=development
   ```

4. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

5. Create a `.env` file in the `frontend` directory with the following content:
   ```
   VITE_API_URL=http://localhost:8080
   ```

## Running the Application

1. Start the backend server:
   ```
   cd backend
   flask run
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

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.

## License

[Specify your chosen license here]

## Acknowledgments

- This project uses OpenAI's API for story generation.
- The frontend is built with Vue.js and uses GSAP for animations.