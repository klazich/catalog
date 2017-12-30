from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    import catalog.models

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from catalog.database import Session
        Session.remove()

    @app.context_processor
    def inject_variables():
        from catalog.helpers import latest_items, get_all_categories
        return dict(
            latest_items=latest_items(10),
            all_categories=get_all_categories())

    @app.template_filter('format_date')
    def format_date_filter(dt):
        return dt.strftime('%B %d %Y %I:%M%p')

    from catalog.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from catalog.read import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
