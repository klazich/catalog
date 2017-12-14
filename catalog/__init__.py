from flask import Flask

from catalog.database import db_session


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    import catalog.models

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from catalog.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
