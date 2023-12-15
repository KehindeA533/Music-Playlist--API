from flask import Flask, request, jsonify
import os
import psycopg2

import random

from dotenv import load_dotenv

# # Load environment variables
load_dotenv()
password = os.getenv("DATABASE_PASSWORD")

# Initialize Flask app
app = Flask(__name__)

# Establish a database connection
connection = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password=password,
)

# Define SQL queries
## CREATE
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

## UPDATE
INSERT_PLAYLIST_DATA = "INSERT INTO playlists (name, creation_date, number_of_songs) VALUES (%s, %s, 0) RETURNING id;"
INSERT_SONG = (
    "INSERT INTO songs (song_name, artist_name, playlist_id) VALUES (%s, %s, %s);"
)

INCREMENT_NUMBER_OF_SONGS = (
    "UPDATE playlists SET number_of_songs = number_of_songs + 1 WHERE id = %s;"
)
DECREMENT_NUMBER_OF_SONGS = (
    "UPDATE playlists SET number_of_songs = number_of_songs - 1 WHERE id = %s;"
)
RESET_NUMBER_OF_SONGS = "UPDATE playlists SET number_of_songs = 0 WHERE id = %s;"

## DELETE
DELETE_ALL_PLAYLISTS = "DROP TABLE IF EXISTS playlists;"
DELETE_PLAYLIST = "DELETE FROM playlists WHERE id = %s;"

DELETE_ALL_SONGS = "DELETE FROM songs WHERE playlist_id = %s;"
DELETE_A_SONG = "DELETE FROM songs WHERE id = %s;"

## READ


# - Create A Playlist
@app.route("/api/playlists", methods=["POST"])
def create_playlist():
    data = request.get_json()
    name = data["name"]
    creation_date = data["creation_date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_PLAYLIST)
            cursor.execute(
                INSERT_PLAYLIST_DATA,
                (
                    name,
                    creation_date,
                ),
            )
            playlist_id = cursor.fetchone()[0]
            cursor.execute(CREATE_SONGS_TABLE)
    return jsonify({"id": playlist_id, "message": f"Playlist {name} created."}), 201


# - Add Song to a Playlist
@app.route("/api/playlists/<int:playlist_id>/songs", methods=["POST"])
def add_song(playlist_id):
    data = request.get_json()
    song_name = data["song_name"]
    artist_name = data["artist_name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_SONG, (song_name, artist_name, playlist_id))
            cursor.execute(INCREMENT_NUMBER_OF_SONGS, (playlist_id,))
    return (
        jsonify({"message": f"Song {song_name} added to playlist {playlist_id}."}),
        201,
    )


# - Delete All Playlist
@app.route("/api/playlists", methods=["DELETE"])
def delete_all_playlist():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ALL_SONGS)
            cursor.execute(DELETE_ALL_PLAYLISTS)
    return "", 204


# - Delete a Individual Playlist
@app.route("/api/playlists/<int:playlist_id>", methods=["DELETE"])
def delete_a_playlist(playlist_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_PLAYLIST, (playlist_id,))
    return "", 204


# - Delete All Songs from a Playlist
@app.route("/api/playlists/<int:playlist_id>/songs", methods=["DELETE"])
def delete_all_songs(playlist_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ALL_SONGS)
    return "", 204


# - Delete A Song from a Playlist
@app.route("/api/playlists/<int:playlist_id>/songs/<int:song_id>", methods=["DELETE"])
def delete_a_song(playlist_id, song_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_A_SONG, (song_id,))
            cursor.execute(
                DECREMENT_NUMBER_OF_SONGS, (playlist_id,)
            )  # - Add a conditional so that it doesnt pass 0

    return "", 204


# - Get All Playlist
@app.route("/api/playlists", methods=["GET"])
def get_all_playlists():
    with connection:
        with connection.cursor() as cursor:
            # Execute a SQL query to fetch all playlists
            cursor.execute("SELECT * FROM playlists;")
            playlists = cursor.fetchall()

    # Convert the playlist data to a list of dictionaries
    playlist_list = []
    for playlist in playlists:
        playlist_dict = {
            "id": playlist[0],
            "name": playlist[1],
            "creation_date": playlist[2],
            "number_of_songs": playlist[3],
        }
        playlist_list.append(playlist_dict)

    return jsonify(playlist_list)


# - Get An Individual Playlist
@app.route("/api/playlists/<int:playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    with connection:
        with connection.cursor() as cursor:
            # Execute a SQL query to fetch an individual playlist by ID
            cursor.execute("SELECT * FROM playlists WHERE id = %s;", (playlist_id,))
            playlist = cursor.fetchone()

    if not playlist:
        return jsonify({"message": "Playlist not found"}), 404

    playlist_dict = {
        "id": playlist[0],
        "name": playlist[1],
        "creation_date": playlist[2],
        "number_of_songs": playlist[3],
    }

    return jsonify(playlist_dict)


# - Get All Song
@app.route("/api/songs", methods=["GET"])
def get_all_songs():
    with connection:
        with connection.cursor() as cursor:
            # Execute a SQL query to fetch all songs
            cursor.execute("SELECT * FROM songs;")
            songs = cursor.fetchall()

    # Convert the song data to a list of dictionaries
    song_list = []
    for song in songs:
        song_dict = {
            "id": song[0],
            "song_name": song[1],
            "artist_name": song[2],
            "playlist_id": song[3],
        }
        song_list.append(song_dict)

    return jsonify(song_list)


# - Get All the songs from a Individual Playlist
@app.route("/api/playlists/<int:playlist_id>/songs", methods=["GET"])
def get_songs_from_playlist(playlist_id):
    with connection:
        with connection.cursor() as cursor:
            # Execute a SQL query to fetch all songs from a specific playlist
            cursor.execute(
                "SELECT * FROM songs WHERE playlist_id = %s;", (playlist_id,)
            )
            songs = cursor.fetchall()

    # Convert the song data to a list of dictionaries
    song_list = []
    for song in songs:
        song_dict = {
            "id": song[0],
            "song_name": song[1],
            "artist_name": song[2],
            "playlist_id": song[3],
        }
        song_list.append(song_dict)

    return jsonify(song_list)


# - Endpoint to Get a Random Song
@app.route("/api/random-song", methods=["GET"])
def get_random_song():
    with connection:
        with connection.cursor() as cursor:
            # Execute a SQL query to count the total number of songs in the database
            cursor.execute("SELECT COUNT(*) FROM songs;")
            total_songs = cursor.fetchone()[0]

            if total_songs == 0:
                return jsonify({"message": "No songs found"}), 404

            # Generate a random song ID within the range of available song IDs
            random_song_id = random.randint(1, total_songs)

            # Execute a SQL query to fetch the random song by ID
            cursor.execute("SELECT * FROM songs WHERE id = %s;", (random_song_id,))
            random_song = cursor.fetchone()

    if not random_song:
        return jsonify({"message": "Random song not found"}), 404

    random_song_dict = {
        "id": random_song[0],
        "song_name": random_song[1],
        "artist_name": random_song[2],
        "playlist_id": random_song[3],
    }

    return jsonify(random_song_dict)
