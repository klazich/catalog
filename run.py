import os

from catalog import create_app
from config import config_obj

# check for environment variable
config_env = os.getenv('FLASK_CONFIG', 'default')
config = config_obj[config_env]

# create flask app with the factory
app = create_app(config)

if app.debug:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# start the server
if __name__ == '__main__':
    app.run()
