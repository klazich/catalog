from catalog.database import db_session
from flask import Flask

app = Flask(__name__)

import catalog.views


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
