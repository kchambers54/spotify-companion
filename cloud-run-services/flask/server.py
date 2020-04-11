import os
import sys

import requests
import spotipy
import spotipy.util

sys.path.append('FlaskSpotifyAuth/')
import startup

from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    """
    Return 
    """
    return 

##################
# Auth Functions #
##################
@app.route('/auth/request/')
def auth_request():
    """
    Requests authorization to access user's data
    """
    response = startup.getUser()
    return redirect(response)

@app.route('/auth/callback/')
def token_request():
    """
    Requests access and refresh tokens.
    Stores those tokens in datastore (TODO, locally for now).
    """
    # Get user access token
    print(request)
    startup.getUserToken(request.args['code'])

    # redirect to homepage
    return redirect('http://localhost:8080/')


#############
# Functions #
#############
@app.route('/functions/playlist-expander/')
def call_playlist_expander():
    return  # call the custom spotipy function here and pass the user's token


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
