import unittest
import json
from app import app, connection  # Import your Flask app and database connection

CREATE_PLAYLIST = """ CREATE TABLE IF NOT EXISTS playlists (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    creation_date TEXT,
    number_of_songs INT
);"""

CREATE_SONGS_TABLE = """CREATE TABLE IF NOT EXISTS songs (
    id SERIAL PRIMARY KEY, 
    song_name TEXT, 
    artist_name TEXT, 
    playlist_id INT,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
);"""


class PlaylistAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_PLAYLIST)
                cursor.execute(CREATE_SONGS_TABLE)

    def tearDown(self):
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS songs")
                cursor.execute("DROP TABLE IF EXISTS playlists")

    def test_create_playlist(self):
        data = {"name": "Test Playlist", "creation_date": "2023-09-24"}
        response = self.app.post("/api/playlists", json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Playlist Test Playlist created.")

    def test_add_song(self):
        playlist_data = {"name": "Test Playlist", "creation_date": "2023-09-24"}
        song_data = {"song_name": "Test Song", "artist_name": "Test Artist"}
        self.app.post("/api/playlists", json=playlist_data)  # Create a playlist
        response = self.app.post("/api/playlists/1/songs", json=song_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Song Test Song added to playlist 1.")

    def test_delete_all_playlist(self):
        playlist_data = {"name": "Test Playlist", "creation_date": "2023-09-24"}
        self.app.post("/api/playlists", json=playlist_data)  # Create a playlist
        response = self.app.delete("/api/playlists")
        self.assertEqual(response.status_code, 204)

    def test_delete_a_playlist(self):
        playlist_data = {"name": "Test Playlist", "creation_date": "2023-09-24"}
        self.app.post("/api/playlists", json=playlist_data)  # Create a playlist
        response = self.app.delete("/api/playlists/1")
        self.assertEqual(response.status_code, 204)

    def test_delete_all_songs(self):
        playlist_data = {"name": "Test Playlist", "creation_date": "2023-09-24"}
        self.app.post("/api/playlists", json=playlist_data)  # Create a playlist
        response = self.app.delete("/api/playlists/1/songs")
        self.assertEqual(response.status_code, 204)

    def test_delete_a_song(self):
        playlist_data = {"name": "Test Playlist", "creation_date": "2023-09-24"}
        song_data = {"song_name": "Test Song", "artist_name": "Test Artist"}
        self.app.post("/api/playlists", json=playlist_data)  # Create a playlist
        self.app.post("/api/playlists/1/songs", json=song_data)  # Add a song
        response = self.app.delete("/api/playlists/1/songs/1")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
