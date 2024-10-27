### INF601 - Advanced Programming in Python
### Damian Rios
### Mini Project 3

from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .db import get_db

library_bp = Blueprint('library', __name__, url_prefix='/library')  # Create a Blueprint for library-related routes


@library_bp.route('/')
def library():
    """Display the user's library."""
    user_id = session.get('user_id')  # Get the logged-in user's ID from the session
    db = get_db()  # Get the database connection
    # Query to get books from the library along with their favorite status and current status
    books = db.execute(
        'SELECT b.*, l.favorite, l.status FROM library l '
        'JOIN book b ON l.book_id = b.id '
        'WHERE l.user_id = ?',
        (user_id,)
    ).fetchall()  # Fetch all books for the user
    return render_template('library/library.html', books=books)  # Render the library template with books


@library_bp.route('/add/<int:book_id>', methods=['GET', 'POST'])
def add_to_library(book_id):
    """Add a book to the user's library."""
    user_id = session.get('user_id')  # Get the logged-in user's ID
    db = get_db()  # Get the database connection
    # Check if the book is already in the user's library
    existing_entry = db.execute(
        'SELECT * FROM library WHERE user_id = ? AND book_id = ?',
        (user_id, book_id)
    ).fetchone()  # Fetch existing entry if it exists

    if existing_entry is None:  # If the book is not in the library
        # Insert a new entry into the library
        db.execute(
            'INSERT INTO library (user_id, book_id) VALUES (?, ?)',
            (user_id, book_id)
        )
        db.commit()  # Commit the changes
        flash('Book added to your library!', 'success')  # Show success message
    else:
        flash('Book is already in your library!', 'info')  # Show info message if the book is already present

    return redirect(url_for('books.view_book', id=book_id))  # Redirect to the book's view page


@library_bp.route('/update_status/<int:book_id>', methods=['POST'])
def update_status(book_id):
    """Update the status of a book in the user's library."""
    user_id = session.get('user_id')  # Get the logged-in user's ID
    status = request.form['status']  # Get the new status from the form
    db = get_db()  # Get the database connection
    # Update the book's status in the library
    db.execute(
        'UPDATE library SET status = ? WHERE user_id = ? AND book_id = ?',
        (status, user_id, book_id)
    )
    db.commit()  # Commit the changes
    flash('Status updated successfully!', 'success')  # Show success message
    return redirect(url_for('library.library'))  # Redirect back to the library


@library_bp.route('/remove/<int:book_id>', methods=['POST'])
def remove_from_library(book_id):
    """Remove a book from the user's library."""
    user_id = session.get('user_id')  # Get the logged-in user's ID
    db = get_db()  # Get the database connection
    # Delete the book from the user's library
    db.execute(
        'DELETE FROM library WHERE user_id = ? AND book_id = ?',
        (user_id, book_id)
    )
    db.commit()  # Commit the changes
    flash('Book removed from your library.', 'success')  # Show success message
    return redirect(url_for('library.library'))  # Redirect back to the library
