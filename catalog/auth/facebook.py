from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from config import FacebookAuthConfig


class FacebookOAuth2(FacebookAuthConfig):
    def __init__(self):
        facebook = OAuth2Session(
            self.CLIENT_ID,
            redirect_uri=self.REDIRECT_URI)
        self.session = facebook_compliance_fix(facebook)
