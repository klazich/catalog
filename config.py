import os
import json


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = ''
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_URI = 'sqlite:///catalog.db'
    CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
    APPLICATION_NAME = 'Catalog App'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

app_dir = os.path.dirname(os.path.abspath(__file__))
