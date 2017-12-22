import os

from catalog import create_app
from config import config

config_type = os.getenv('FLASK_CONFIG', 'default')

app = create_app(config[config_type])

if __name__ == '__main__':
    app.run()
