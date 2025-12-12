import unittest
import json
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, MOCK_PLAYLISTS

class TestPlaylistAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_generate_playlist_pop(self):
        response = self.app.post('/api/generate', 
                                 data=json.dumps({"genre": "Pop"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['genre'], "Pop")
        self.assertTrue(len(data['playlist']) > 0)
        # Should return mock data if no API key
        if "HF_API_KEY" not in os.environ:
             self.assertEqual(data['playlist'][0]['title'], MOCK_PLAYLISTS["Pop"][0]["title"])

    def test_generate_playlist_unknown(self):
        response = self.app.post('/api/generate', 
                                 data=json.dumps({"genre": "Unknown"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['genre'], "Unknown")
        self.assertTrue(len(data['playlist']) > 0)
        self.assertIn("Generic Unknown Song", data['playlist'][0]['title'])

    def test_generate_playlist_no_genre(self):
        response = self.app.post('/api/generate', 
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
