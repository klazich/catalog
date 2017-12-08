from flask import Flask

from catalog.database import db_session


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    import catalog.views

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    import catalog.models

    app.register_blueprint(catalog.views.home)

    return app
