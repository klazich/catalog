from flask import Flask

from catalog.database import Database
from config import app_dir

db = Database(app_dir)


def create_app():
    app = Flask(__name__)

    import catalog.views

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    import catalog.models

    app.register_blueprint(catalog.views.home)

    return app
