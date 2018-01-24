from flask import Flask


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    import catalog.models

    # api endpoints with Flask-Restless:
    #   <host>:<port>/api/items
    #   <host>:<port>/api/categories
    from catalog.api import manager
    manager.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from catalog.database import session
        session.remove()

    @app.context_processor
    def inject_variables():
        from .database import session
        from .models import Category
        return dict(
            all_categories=session.query(Category).all())

    @app.template_filter('format_date')
    def format_date_filter(dt):
        return dt.strftime('%B %d, %Y')

    from catalog.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    from catalog.views.catalog import catalog_bp
    app.register_blueprint(catalog_bp)

    from catalog.views.category import category_bp
    app.register_blueprint(category_bp)

    from catalog.views.item import item_bp
    app.register_blueprint(item_bp)

    return app
