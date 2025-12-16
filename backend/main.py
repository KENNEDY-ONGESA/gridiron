import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock data for fallback
MOCK_PLAYLISTS = {
    "Pop": [
        {"title": "Shape of You", "artist": "Ed Sheeran"},
        {"title": "Blinding Lights", "artist": "The Weeknd"},
        {"title": "Levitating", "artist": "Dua Lipa"},
        {"title": "Stay", "artist": "The Kid LAROI & Justin Bieber"},
        {"title": "Bad Guy", "artist": "Billie Eilish"}
    ],
    "Rock": [
        {"title": "Bohemian Rhapsody", "artist": "Queen"},
        {"title": "Hotel California", "artist": "Eagles"},
        {"title": "Smells Like Teen Spirit", "artist": "Nirvana"},
        {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses"},
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin"}
    ],
    "Jazz": [
        {"title": "Take Five", "artist": "Dave Brubeck"},
        {"title": "So What", "artist": "Miles Davis"},
        {"title": "Fly Me To The Moon", "artist": "Frank Sinatra"},
        {"title": "What A Wonderful World", "artist": "Louis Armstrong"},
        {"title": "My Favorite Things", "artist": "John Coltrane"}
    ]
}

def generate_playlist_with_ai(genre):
    """
    Generates a playlist using Hugging Face Inference API.
    Expects HF_API_KEY env variable.
    """
    api_key = os.environ.get("HF_API_KEY")
    if not api_key:
        print("No HF_API_KEY found. Using mock data.")
        return None

    # Using a model that is good at following instructions, e.g., mistralai/Mistral-7B-Instruct-v0.2 or similar
    # For simplicity, we'll try to use a popular text generation model.
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3" 
    # Fallback to a smaller model if that one is not available or requires pro subscription for some reason
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    prompt = f"""
    Generate a playlist of 5 songs for the genre: {genre}.
    Return the output ONLY as a valid JSON array of objects, where each object has "title" and "artist".
    Do not include any other text or explanation.
    Example format:
    [
        {{"title": "Song Name", "artist": "Artist Name"}}
    ]
    """

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "return_full_text": False,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Depending on the model, the output might be in different formats.
        # Mistral/Llama usually returns [{'generated_text': '...'}]
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            generated_text = result[0]['generated_text']
            # Attempt to parse JSON from the generated text
            # Sometimes models add markdown code blocks like ```json ... ```
            cleaned_text = generated_text.strip()
            if "```json" in cleaned_text:
                cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_text:
                cleaned_text = cleaned_text.split("```")[1].strip()
            
            return json.loads(cleaned_text)
            
    except Exception as e:
        print(f"Error calling AI API: {e}")
        return None
    
    return None

@app.route('/api/generate', methods=['POST'])
def generate_playlist():
    data = request.json
    if not data or 'genre' not in data:
        return jsonify({"error": "Genre is required"}), 400
    
    genre = data['genre']
    
    # Try AI generation first
    playlist = generate_playlist_with_ai(genre)
    
    # Fallback to mock data if AI fails or returns nothing
    if not playlist:
        # Check if we have exact match in mock
        if genre in MOCK_PLAYLISTS:
            playlist = MOCK_PLAYLISTS[genre]
        else:
            # Generic fallback
            playlist = [
                {"title": f"Generic {genre} Song 1", "artist": "Unknown Artist"},
                {"title": f"Generic {genre} Song 2", "artist": "Unknown Artist"},
                {"title": f"Generic {genre} Song 3", "artist": "Unknown Artist"},
                {"title": f"Generic {genre} Song 4", "artist": "Unknown Artist"},
                {"title": f"Generic {genre} Song 5", "artist": "Unknown Artist"}
            ]
            
    return jsonify({"genre": genre, "playlist": playlist})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
