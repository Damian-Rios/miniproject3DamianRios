### INF601 - Advanced Programming in Python
### Damian Rios
### Mini Project 3

import sqlite3
import click
from flask import current_app, g

def get_db():
    """Get a database connection from the Flask app context."""
    # Check if a database connection already exists in the Flask context
    if 'db' not in g:
        # Create a new database connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],  # Use the database path from the app's config
            detect_types=sqlite3.PARSE_DECLTYPES  # Enable parsing of specific types
        )
        g.db.row_factory = sqlite3.Row  # Set row factory to return rows as dictionaries

    return g.db  # Return the database connection


def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)  # Remove the database connection from the Flask context

    if db is not None:  # If the connection exists, close it
        db.close()


def init_db():
    """Initialize the database with the schema defined in schema.sql."""
    db = get_db()  # Get the database connection

    # Open the schema.sql file and execute its contents to create tables
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))  # Execute the SQL script


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()  # Call the function to initialize the database
    click.echo('Initialized the database.')  # Print a confirmation message


def init_app(app):
    """Register database-related functions with the Flask app."""
    app.teardown_appcontext(close_db)  # Register the close_db function to be called when the app context ends
    app.cli.add_command(init_db_command)  # Add the init-db command to the Flask CLI
