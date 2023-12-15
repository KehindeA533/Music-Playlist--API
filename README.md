# Music Playlist API

This is a simple Flask-based API for managing music playlists and songs. You can use this API to create playlists, add songs to playlists, delete playlists and songs, and retrieve information about playlists and songs.

## Prerequisites

Before you get started, make sure you have the following installed:

-     Python
-     Flask
-     psycopg2 (for PostgreSQL database connectivity)

## Setup

1. Clone this repository to your local machine.
2. Create a PostgreSQL database with the following details:
   - Host: localhost
   - Database Name: postgres
   - Username: postgres
   - Password: "INSERT YOUR OWN POSTGRES PASSWORD"
3. Initialize the Flask app by running the flask:
   `FLASK RUN`

## API Endpoints

### 1. Create a Playlist

- Endpoint: /api/playlists (POST)
- Description: Create a new playlist.
- Request Body: `{
    "name": "My Playlist",
    "creation_date": "2023-09-25"
}
`

### 2. Add Song to a Playlist

### 3. Delete All Playlists

### 4. Delete an Individual Playlist

### 5. Delete All Songs from a Playlist

### 6. Delete a Song from a Playlist

### 7. Get All Playlists (Not Implemented Yet)

### 8. Get an Individual Playlist (Not Implemented Yet)

### 9. Get All Songs (Not Implemented Yet)

### 10. Get All Songs from an Individual Playlist (Not Implemented Yet)
