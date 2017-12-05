from os.path import exists

from catalog.database import init_db
from catalog import app

if __name__ == '__main__':
    if not exists('./catalog.db'):
        init_db(populate=True)
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=5000)
