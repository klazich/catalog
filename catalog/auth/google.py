from requests_oauthlib import OAuth2Session

from config import GoogleAuthConfig


class GoogleOAuth2(GoogleAuthConfig):
    def __init__(self):
        self.session = OAuth2Session(
            self.CLIENT_ID,
            scope=self.SCOPE,
            redirect_uri=self.REDIRECT_URI)
