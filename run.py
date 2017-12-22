from catalog import create_app
from config import config

app = create_app(config['dev'])

if __name__ == '__main__':
    app.run()
