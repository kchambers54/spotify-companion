from flask_spotify_auth import getAuth, refreshAuth, getToken
from SpotToken import SpotToken
import config

# Client ID FROM SPOTIFY
CLIENT_ID = config.CLIENT_ID

# CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = config.CLIENT_SECRET

# Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = "playlist-modify-public playlist-read-private"

#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
# TODO May need to externalize this to datastore

def getUserCode():
    return getAuth(CLIENT_ID, "{}:{}/auth/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    """
    X
    :arg code: Code received from spotify API after user login
    :return: 
    """
    # global TOKEN_DATA  # Externalize to datastore
    token_data = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/auth/callback/".format(CALLBACK_URL, PORT))
    # MODIFED - Returning token to Flask #
    return token_data
    # END MODIFIED #

def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA
