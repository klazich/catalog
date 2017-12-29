import os

basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class BaseConfig:
    APP_NAME = 'FSND Catalog App'
    SECRET_KEY = os.environ.get("SECRET_KEY") or b'\x1dLK!\xa9\xa3VwJ&j\x97l\x07(\x08M\x97PV\xc8g\xe8\xcd'


class GoogleAuthConfig(BaseConfig):
    PROVIDER = 'google'
    CLIENT_ID = '288467794624-ol9d6dpr3fccs8v0olhpbp1r6ots6sf7.apps.googleusercontent.com'
    CLIENT_SECRET = 'Y3e7-a3KD3ez9P8-AZw1N0Bz'
    AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    REDIRECT_URI = 'http://localhost:5000/callback/google'
    USER_INFO = 'https://www.googleapis.com/oauth2/v3/userinfo'
    SCOPE = ["https://www.googleapis.com/auth/userinfo.email",
             "https://www.googleapis.com/auth/userinfo.profile"]


class FacebookAuthConfig(BaseConfig):
    PROVIDER = 'facebook'
    CLIENT_ID = '1273316589480067'
    CLIENT_SECRET = 'efd08abe7ac83d5f05777ce2f07a1bb2'
    AUTHORIZATION_BASE_URL = 'https://www.facebook.com/dialog/oauth'
    TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
    REDIRECT_URI = 'http://localhost:5000/callback/facebook'
    USER_INFO = 'https://graph.facebook.com/'
    SCOPE = None


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'catalog.dev.db')


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'catalog.test.db')


class ProdConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "catalog.db")


config_obj = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
