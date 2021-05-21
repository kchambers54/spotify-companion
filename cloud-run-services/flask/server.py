import os
import sys
import logging

import requests
import spotipy
import spotipy.util

sys.path.append('FlaskSpotifyAuth/')
import startup

from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = 'LKsdfsdf897769879sDSFSDFsdfsdkljdfhgkKLJHLKJH897687f'  # TODO - externalize


@app.route('/')
def index():
    """
    Return 
    """
    try:
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
    response = startup.getUser()
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

    # Save token data to session
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
    return  # call the custom spotipy function here and pass the user's token

########
# Main #
########
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
