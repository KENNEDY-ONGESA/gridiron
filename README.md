# Music Playlist Generator

A web application that generates music playlists based on a selected genre using AI.

## Features

- **Frontend**: Vue.js application with a clean interface to select genres and view playlists.
- **Backend**: Flask API that generates playlists using Hugging Face Inference API (or mock data if API key is missing).
- **AI Integration**: Uses Large Language Models (LLM) to generate song recommendations.

## Prerequisites

- Node.js (v18+)
- Python (v3.8+)

## Quick Start

1. Clone the repository.
2. Run the start script:

   ```bash
   ./start.sh
   ```

   This script will:
   - Create a Python virtual environment and install backend dependencies.
   - Install Node.js dependencies.
   - Start both the Flask backend (port 5000) and Vue frontend (port 5173).

3. Open your browser to `http://localhost:5173`.

## Configuration

### AI API Key (Optional)

To use the real AI generation, you need a Hugging Face API Token.

1. Get a token from [Hugging Face](https://huggingface.co/settings/tokens).
2. Export it as an environment variable before running the script:

   ```bash
   export HF_API_KEY="your_token_here"
   ./start.sh
   ```

If no key is provided, the application will use a fallback mock generator with predefined playlists.

## Project Structure

- `backend/`: Flask application
  - `main.py`: API entry point and logic
  - `requirements.txt`: Python dependencies
- `frontend/`: Vue.js application
  - `src/`: Source code
  - `package.json`: Node dependencies
- `start.sh`: Helper script to run the project

## API Endpoint

**POST** `/api/generate`

Body:
```json
{
  "genre": "Pop"
}
```

Response:
```json
{
  "genre": "Pop",
  "playlist": [
    {
      "title": "Song Title",
      "artist": "Artist Name"
    },
    ...
  ]
}
```
