import os
from datetime import datetime
from flask import Flask


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bookNest.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    from .db import init_app
    init_app(app)

    # Register Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Handles authentication

    from .dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # User dashboard

    from .book import books_bp
    app.register_blueprint(books_bp, url_prefix='/books')  # Handles book creation and modification

    from .review import review_bp
    app.register_blueprint(review_bp, url_prefix='/review')

    # Add the root URL (index) rule
    app.add_url_rule('/', endpoint='dashboard.index')

    # Add context processor
    @app.context_processor
    def inject_now():
        return {'current_year': datetime.utcnow().year}

    return app
