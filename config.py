import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    APP_NAME = 'FSND Catalog App'
    SECRET_KEY = os.environ.get("SECRET_KEY") or b'\x1dLK!\xa9\xa3VwJ&j\x97l\x07(\x08M\x97PV\xc8g\xe8\xcd'


class GoogleAuthConfig(BaseConfig):
    """ Google OAuth2 configuration """
    PROVIDER = 'google'
    CLIENT_ID = '288467794624-ol9d6dpr3fccs8v0olhpbp1r6ots6sf7.apps.googleusercontent.com'
    CLIENT_SECRET = 'Y3e7-a3KD3ez9P8-AZw1N0Bz'
    AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
    REFRESH_URL = 'https://accounts.google.com/o/oauth2/token'
    REDIRECT_URI = 'http://localhost:5000/auth/callback'
    USER_INFO = 'https://www.googleapis.com/oauth2/v3/userinfo'
    SCOPE = ["https://www.googleapis.com/auth/userinfo.email",
             "https://www.googleapis.com/auth/userinfo.profile"]


class FacebookAuthConfig(BaseConfig):
    """ Facebook OAuth2 configuration """
    PROVIDER = 'facebook'
    CLIENT_ID = '1273316589480067'
    CLIENT_SECRET = 'efd08abe7ac83d5f05777ce2f07a1bb2'
    AUTHORIZATION_BASE_URL = 'https://www.facebook.com/dialog/oauth'
    TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
    REDIRECT_URI = 'http://localhost:5000/auth/callback'
    USER_INFO = 'https://graph.facebook.com/me?fields=id,name,email'
    SCOPE = ''


class DevConfig(BaseConfig):
    """ Development flask configuration: debug on, testing off, db is catalog.dev.db """
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'catalog.dev.db')


class TestConfig(BaseConfig):
    """ Testing flask configuration: debug on, testing on, db is catalog.test.db """
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'catalog.test.db')


class ProdConfig(BaseConfig):
    """ Production flask configuration: debug off, testing off, db is catalog.db """
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "catalog.db")


config_obj = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig}
