### INF601 - Advanced Programming in Python
### Damian Rios
### Mini Project 3

from flask import Blueprint, g, render_template, request, redirect, url_for, session, flash
from .db import get_db
from bookNest.auth import login_required

# Create a Blueprint for the books functionality
books_bp = Blueprint('books', __name__, url_prefix='/books')

# Route to add a new book
@books_bp.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':  # Check if the request is POST
        # Retrieve form data
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']
        user_id = g.user['id']  # Get the current logged-in user's ID

        # Validate that all fields are filled out
        if not title or not author or not genre or not description:
            flash('All fields are required!')  # Flash an error message
        else:
            db = get_db()  # Get the database connection
            # Insert the new book into the database
            db.execute(
                'INSERT INTO book (title, author, genre, description, user_id) VALUES (?, ?, ?, ?, ?)',
                (title, author, genre, description, user_id)
            )
            db.commit()  # Commit the changes to the database
            flash('Book added successfully!')  # Flash a success message
            return redirect(url_for('dashboard.index'))  # Redirect to the dashboard

    return render_template('books/addBook.html')  # Render the add book form


# Route to delete a book by its ID
@books_bp.route('/delete/<int:id>', methods=('POST',))
def delete_book(id):
    db = get_db()  # Get the database connection
    # Delete the book with the specified ID
    db.execute('DELETE FROM book WHERE id = ?', (id,))
    db.commit()  # Commit the changes to the database
    flash('Book deleted successfully!')  # Flash a success message
    return redirect(url_for('dashboard.index'))  # Redirect to the dashboard


# Route to view a specific book by its ID
@books_bp.route('/view/<int:id>')
@login_required  # Ensure the user is logged in before accessing this route
def view_book(id):
    db = get_db()  # Get the database connection
    user_id = session.get('user_id')  # Get the current logged-in user ID

    # Get the book details from the database
    book = db.execute('SELECT * FROM book WHERE id = ?', (id,)).fetchone()
    if book is None:  # Check if the book exists
        flash('Book not found.')  # Flash an error message
        return redirect(url_for('dashboard.index'))  # Redirect to the dashboard

    # Get all reviews for the book along with the usernames of reviewers
    reviews = db.execute(
        'SELECT r.id, r.rating, r.review_text, r.created_at, u.username FROM review r '
        'JOIN user u ON r.user_id = u.id WHERE r.book_id = ?',
        (id,)
    ).fetchall()

    # Check if the current user has already reviewed this book
    user_review = db.execute(
        'SELECT id FROM review WHERE user_id = ? AND book_id = ?',
        (user_id, id)
    ).fetchone()

    # Calculate the average rating of the book
    avg_rating_row = db.execute(
        'SELECT COALESCE(AVG(r.rating), 0) AS avg_rating FROM review r WHERE r.book_id = ?',
        (id,)
    ).fetchone()
    avg_rating = avg_rating_row['avg_rating'] if avg_rating_row else None  # Get the average rating

    return render_template(
        'books/viewBook.html',
        book=book,  # Pass the book details to the template
        reviews=reviews,  # Pass the reviews to the template
        avg_rating=avg_rating,  # Pass the average rating to the template
        user_review=user_review  # Pass the user's review ID if it exists
    )


# Route to update an existing book by its ID
@books_bp.route('/update/<int:id>', methods=('GET', 'POST'))
def update_book(id):
    db = get_db()  # Get the database connection
    # Get the current details of the book
    book = db.execute('SELECT * FROM book WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':  # Check if the request is POST
        # Retrieve updated form data
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']  # Get the updated description

        # Validate that all fields are filled out
        if not title or not author or not genre or not description:
            flash('All fields are required!')  # Flash an error message
        else:
            # Update the book details in the database
            db.execute(
                'UPDATE book SET title = ?, author = ?, genre = ?, description = ? WHERE id = ?',
                (title, author, genre, description, id)
            )
            db.commit()  # Commit the changes to the database
            flash('Book updated successfully!')  # Flash a success message
            return redirect(url_for('dashboard.index'))  # Redirect to the dashboard

    return render_template('books/updateBook.html', book=book)  # Render the update book form
