import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class GoogleAuth:
    CLIENT_ID = '288467794624-ol9d6dpr3fccs8v0olhpbp1r6ots6sf7.apps.googleusercontent.com'
    CLIENT_SECRET = 'Y3e7-a3KD3ez9P8-AZw1N0Bz'
    REDIRECT_URI = 'https://localhost:5000/oauth2calback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ["https://www.googleapis.com/auth/userinfo.email",
             "https://www.googleapis.com/auth/userinfo.profile"]


class FacebookAuth:
    pass


class BaseConfig:
    APP_NAME = 'FSND Catalog App'
    SECRET_KEY = os.environ.get("SECRET_KEY") or b'\x1dLK!\xa9\xa3VwJ&j\x97l\x07(\x08M\x97PV\xc8g\xe8\xcd'


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


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
