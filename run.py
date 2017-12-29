import os

from catalog import create_app
from config import config_obj

config_env = os.getenv('FLASK_CONFIG', 'default')
config = config_obj[config_env]

app = create_app(config)

if app.debug:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if __name__ == '__main__':
    app.run()
