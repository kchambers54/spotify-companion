import os
import sys
import logging

import requests
import spotipy
import spotipy.util

sys.path.append('FlaskSpotifyAuth/')
import startup
import config
sys.path.append('Functions')
import playlist_expander

from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY


@app.route('/')
def index():
    """
    Return 
    """
    try:
        # Temporary
        return session['token_data']
    except:

        return 'HOME PAGE'

##################
# Auth Functions #
##################
@app.route('/auth/request/')
def auth_request():
    """
    Requests authorization to access user's data
    """
    response = startup.getUserCode()
    return redirect(response)

@app.route('/auth/callback/')
def token_request():
    """
    Requests access and refresh tokens.
    Stores those tokens in datastore (TODO, locally for now).
    """
    # Get user access token and refresh token
    print(request, file=sys.stderr)
    token_data = startup.getUserToken(request.args['code'])

    print('Token Data:\n')
    print(token_data, file=sys.stderr)

    # Save token data to session for now TODO: store somewhere backend
    session['token_data'] = token_data.get_dict()

    # redirect to homepage
    return redirect('http://localhost:5000/')

@app.route('/auth/logout/')
def auth_logout():
    session.pop('token_data')

    return "LOGGED OUT"


#############
# Functions #
#############
@app.route('/functions/playlist-expander/')
def call_playlist_expander():
    """
    Call the "playlist expander" function, creating a new playlist with the top X 
    songs from each artist in an existing playlist
    """
    if session.get('token_data') is not None:

        source_playlist_name = request.args.get('source_playlist_name')
        try:  # Default = 10
            num_tracks_per_artist = int(request.args['num_tracks'])
        except:
            num_tracks_per_artist = 10

        function_response = playlist_expander.execute(session.get('token_data').get('access_token'), source_playlist_name, num_tracks_per_artist)

        return function_response
    else:
        print('No auth token available to call playlist expander')
        return "No auth token available to call playlist expander.  Please login."

########
# Main #
########
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
