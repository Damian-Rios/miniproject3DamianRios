from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'yoursecretkey'


# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('yourdatabase.db')
    conn.row_factory = sqlite3.Row
    return conn


# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                         (username, email, hashed_password))
            conn.commit()
            return redirect('/login')  # Redirect to login after successful registration
        except sqlite3.IntegrityError:
            return 'Username or email already exists'  # Handle duplicate usernames/emails
        finally:
            conn.close()

    return render_template('register.html')
