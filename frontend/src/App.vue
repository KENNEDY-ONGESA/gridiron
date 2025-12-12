<template>
  <div class="container">
    <h1>Music Playlist Generator</h1>
    
    <div class="controls">
      <label for="genre-select">Select Genre:</label>
      <select id="genre-select" v-model="selectedGenre">
        <option disabled value="">Please select one</option>
        <option>Pop</option>
        <option>Rock</option>
        <option>Jazz</option>
        <option>Hip Hop</option>
        <option>Classical</option>
        <option>Electronic</option>
        <option>Country</option>
        <option>R&B</option>
      </select>
      
      <button @click="generatePlaylist" :disabled="!selectedGenre || loading">
        {{ loading ? 'Generating...' : 'Generate Playlist' }}
      </button>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="playlist.length > 0" class="playlist-container">
      <h2>{{ currentGenre }} Playlist</h2>
      <ul class="playlist">
        <li v-for="(song, index) in playlist" :key="index" class="song-item">
          <span class="song-title">{{ song.title }}</span>
          <span class="song-artist">by {{ song.artist }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedGenre: '',
      currentGenre: '',
      playlist: [],
      loading: false,
      error: null
    };
  },
  methods: {
    async generatePlaylist() {
      if (!this.selectedGenre) return;
      
      this.loading = true;
      this.error = null;
      this.playlist = [];
      this.currentGenre = this.selectedGenre;

      try {
        // Since we configured proxy in vite.config.js, we can call /api directly
        // However, if running in a different environment, we might need the full URL.
        // For development with the proxy, this works.
        const response = await axios.post('/api/generate', {
          genre: this.selectedGenre
        });
        
        this.playlist = response.data.playlist;
      } catch (err) {
        console.error(err);
        this.error = "Failed to generate playlist. Please try again.";
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

select {
  padding: 0.6em 1.2em;
  font-size: 1em;
  border-radius: 8px;
  border: 1px solid transparent;
  background-color: #1a1a1a;
  color: white;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: #646cff;
  cursor: pointer;
  transition: border-color 0.25s;
}

button:hover {
  border-color: #646cff;
}

button:disabled {
  background-color: #3a3a3a;
  cursor: not-allowed;
}

.playlist-container {
  width: 100%;
  max-width: 600px;
  background-color: #1a1a1a;
  border-radius: 12px;
  padding: 2rem;
}

.playlist {
  list-style: none;
  padding: 0;
  text-align: left;
}

.song-item {
  padding: 10px;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
}

.song-item:last-child {
  border-bottom: none;
}

.song-title {
  font-weight: bold;
}

.song-artist {
  color: #aaa;
}

.error {
  color: #ff6b6b;
}
</style>
