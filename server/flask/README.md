# spotify-companion Flask server

To run the spotify companion Flask server locally in a test / dev scenario, follow these steps:
1. pip install flask, pip install spotipy
2. In "cloud-run-services/flask/", run:
    - $ export FLASK_APP=server.py
    - $ flask run
3. Reach the server at "localhost:5000"
4. Sign in at localhost:5000/auth/request/

You can call the playlist-expander at "localhost:5000/functions/playlist-expander/?source_playlist_name=<PLAYLIST NAME>&num_tracks=10"
    - The response will contain the song and artist list of the new playlist