

class SpotToken:

    def __init__(self, response):
        self.access_token = response.get("access_token")
        self.token_type = response.get('token_type')
        self.expires_in = response.get('expires_in')
        self.refresh_token = response.get('refresh_token')  # Can be None
        self.scope = response.get('scope')
        self.auth_head = {"Authorization": self.token_type + " " + self.access_token}

    def get_dict(self):
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "scope": self.scope,
            "auth_head": self.auth_head
        }