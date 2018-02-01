from flask import Flask


def create_app(config_obj):
    """
    Flask application factory for creating app instances

    :param config_obj:
    :return:
    :rtype:
    """
    app = Flask(__name__)
    app.config.from_object(config_obj)

    import catalog.models

    # api endpoints with Flask-Restless:
    from catalog.api import manager
    manager.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """See: http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/"""
        from catalog.database import session
        session.remove()

    @app.template_filter('format_date')
    def format_date_filter(dt):
        """A Jinja2 filter to format date in templates"""
        return dt.strftime('%B %d, %Y')

    # register blueprints
    from catalog.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    from catalog.views.catalog import catalog_bp
    app.register_blueprint(catalog_bp)

    from catalog.views.category import category_bp
    app.register_blueprint(category_bp)

    from catalog.views.item import item_bp
    app.register_blueprint(item_bp)

    return app
