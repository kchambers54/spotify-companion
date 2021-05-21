from flask_spotify_auth import getAuth, refreshAuth, getToken
from SpotToken import SpotToken

#Add your client ID TODO Remove
CLIENT_ID = "a9d83f4e8e0d4276bd0f49f86fd8a0a9"

#aDD YOUR CLIENT SECRET FROM SPOTIFY TODO Remove
CLIENT_SECRET = "611bf898debf40db95ffdb3d136b91d8"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = "playlist-modify-public playlist-read-private"

#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
# TODO May need to externalize this to datastore
# TOKEN_DATA = []


def getUser():
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
