### INF601 - Advanced Programming in Python
### Damian Rios
### Mini Project 3

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from bookNest.db import get_db

# Create a blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route for user registration
@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':  # Check if the form has been submitted
        username = request.form['username']  # Get the username from the form
        password = request.form['password']  # Get the password from the form
        firstname = request.form['firstname']  # Get the first name from the form
        lastname = request.form['lastname']  # Get the last name from the form
        db = get_db()  # Get a database connection
        error = None  # Initialize an error variable

        # Validate form inputs
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'

        # If no errors, proceed with registration
        if error is None:
            try:
                # Insert the new user into the database
                db.execute(
                    "INSERT INTO user (username, password, firstname, lastname) VALUES (?, ?, ?, ?)",
                    (username, generate_password_hash(password), firstname, lastname)
                )
                db.commit()  # Commit the transaction
            except db.IntegrityError:
                # Handle case where the username is already registered
                error = f"User {username} is already registered."
            else:
                # Redirect to the login page after successful registration
                return redirect(url_for("auth.login"))

        # Flash an error message to the user if registration fails
        flash(error)

    # Render the registration template
    return render_template('auth/register.html')

# Route for user login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':  # Check if the form has been submitted
        username = request.form['username']  # Get the username from the form
        password = request.form['password']  # Get the password from the form
        db = get_db()  # Get a database connection
        error = None  # Initialize an error variable
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()  # Fetch the user record from the database

        # Validate login credentials
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # If no errors, log the user in
        if error is None:
            session.clear()  # Clear any existing session data
            session['user_id'] = user['id']  # Store the user's ID in the session
            return redirect(url_for('dashboard.index'))  # Redirect to the dashboard

        # Flash an error message if login fails
        flash(error)

    # Render the login template
    return render_template('auth/login.html')

# Function to load the logged-in user before each request
@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')  # Get the user ID from the session

    if user_id is None:
        g.user = None  # No user is logged in
    else:
        # Fetch the user record from the database
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# Route for logging out the user
@auth_bp.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return redirect(url_for('auth.login'))  # Redirect to the login page

# Decorator to require login for certain views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:  # Check if the user is logged in
            return redirect(url_for('auth.login'))  # Redirect to the login page if not

        return view(**kwargs)  # Call the original view if the user is logged in

    return wrapped_view
