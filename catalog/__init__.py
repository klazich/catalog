from flask import Flask, current_app

from catalog.database import db_session
from catalog.helpers import latest_items


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    import catalog.models

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.context_processor
    def inject_latest_items():
        return dict(latest_items=latest_items(40))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from catalog.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
