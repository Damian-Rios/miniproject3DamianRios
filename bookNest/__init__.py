import os
from flask import Flask
from .db import init_db
from .auth import auth_bp
from .dashboard import dashboard_bp


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
    init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Handles registration, login, etc.
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # Handles user dashboard

    # Add the root URL (index) rule
    app.add_url_rule('/', endpoint='index')

    return app