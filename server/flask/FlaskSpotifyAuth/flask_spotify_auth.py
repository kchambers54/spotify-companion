import base64, json, requests
from SpotToken import SpotToken

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''
    

def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
    return data


def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    auth_header = get_auth_header(client_id, client_secret) 

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=auth_header)

    return handleToken(json.loads(post.text))
    

def handleToken(response):
    token_object = SpotToken(response)

    return token_object


def refreshAuth():
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : REFRESH_TOKEN
    }

    auth_header = get_auth_header(client_id, client_secret)

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=auth_header)
    p_back = json.dumps(post_refresh.text)
    
    return handleToken(p_back)


def get_auth_header(client_id, client_secret):
    auth_str = bytes('{}:{}'.format(client_id, client_secret), 'utf-8')
    encoded_id_and_secret = base64.b64encode(auth_str).decode('utf-8')
    
    return {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded_id_and_secret)}