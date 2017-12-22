from requests_oauthlib import OAuth2Session
# https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html

from config import GoogleAuth

google = OAuth2Session(
    GoogleAuth.CLIENT_ID,
    scope=GoogleAuth.SCOPE,
    redirect_uri=GoogleAuth.REDIRECT_URI)

authorization_url, state = google.authorization_url(
    GoogleAuth.AUTH_URI,
    access_type='offline',
    prompt='select_account')


class OAuth2(GoogleAuth):
    state = state
    authorization_url = authorization_url
