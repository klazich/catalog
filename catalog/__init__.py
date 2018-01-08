from flask import Flask


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

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
        return dt.strftime('%B %d, %Y')

    from catalog.views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from catalog.views.create import create as create_blueprint
    app.register_blueprint(create_blueprint)

    from catalog.views.read import read as read_blueprint
    app.register_blueprint(read_blueprint)

    from catalog.views.delete import delete as delete_blueprint
    app.register_blueprint(delete_blueprint)

    # from catalog.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)
    #
    # from catalog.create import create as create_blueprint
    # app.register_blueprint(create_blueprint)

    return app
