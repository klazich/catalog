from catalog import create_app
from catalog.database import init_db, seed_db
from config import app_config

config = app_config['development']

app = create_app(config)

if __name__ == '__main__':
    app.debug = True
    app.run()
