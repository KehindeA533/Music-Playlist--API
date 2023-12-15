from app import app, connection

cursor = connection.cursor()
CREATE_PLAYLIST = """ CREATE TABLE IF NOT EXISTS playlists (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    creation_date TEXT,
    number_of_songs INT
);"""

<<<<<<< HEAD
CREATE_SONGS_TABLE = """CREATE TABLE IF NOT EXISTS songs (
    id SERIAL PRIMARY KEY, 
    song_name TEXT, 
    artist_name TEXT, 
    playlist_id INT,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
);"""

=======
>>>>>>> ac093fe5349c6fb56ab6cfa39c81b1658cd29986
# Define an SQL statement to insert data
INSERT_PLAYLIST_DATA = "INSERT INTO playlists (name, creation_date, number_of_songs) VALUES (%s, %s, 0) RETURNING id;"

# Data to insert
data_to_insert = [
<<<<<<< HEAD
    {"name": "Black", "creation_date": "02/01/2023"},
    {"name": "Blue", "creation_date": "07/20/2022"},
    {"name": "Red", "creation_date": "12/03/2022"},
    {"name": "Green", "creation_date": "05/13/2014"},
    {"name": "Yellow", "creation_date": "09/27/2023"},
=======
>>>>>>> ac093fe5349c6fb56ab6cfa39c81b1658cd29986
]


# Create Playlist
cursor.execute(CREATE_PLAYLIST)
<<<<<<< HEAD
cursor.execute(CREATE_SONGS_TABLE)
=======
>>>>>>> ac093fe5349c6fb56ab6cfa39c81b1658cd29986

# Loop through the data and execute the INSERT statement
for data in data_to_insert:
    values = (data["name"], data["creation_date"])
    cursor.execute(INSERT_PLAYLIST_DATA, values)

# ---------------------------------------------------------
# ---------------------------------------------------------
CREATE_SONGS_TABLE = """CREATE TABLE IF NOT EXISTS songs (
    id SERIAL PRIMARY KEY, 
    song_name TEXT, 
    artist_name TEXT, 
    playlist_id INT,
    FOREIGN KEY(playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
);"""


# Commit the changes and close the cursor
connection.commit()
cursor.close()
