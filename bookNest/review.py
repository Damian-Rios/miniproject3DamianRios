from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from bookNest.auth import login_required
from bookNest.db import get_db

review_bp = Blueprint('review', __name__, url_prefix='/review')  # Create a Blueprint for review-related routes


@review_bp.route('/create/<int:book_id>', methods=('GET', 'POST'))
@login_required  # Ensure the user is logged in to create a review
def create(book_id):
    db = get_db()  # Get the database connection
    # Retrieve the book title based on the book_id
    book = db.execute('SELECT title FROM book WHERE id = ?', (book_id,)).fetchone()

    # Check if the book exists
    if book is None:
        abort(404, f"Book with ID {book_id} does not exist.")  # Return a 404 error if the book does not exist

    book_title = book['title']  # Extract the book title from the query result

    if request.method == 'POST':  # Handle form submission
        review_text = request.form['review_text']  # Get the review text from the form
        rating = request.form['rating']  # Get the rating from the form
        user_id = session.get('user_id')  # Get the logged-in user's ID from the session
        error = None  # Initialize error variable

        # Validate the review text and rating
        if not review_text:
            error = 'Review text is required.'  # Check if review text is provided
        elif not rating or not (1 <= int(rating) <= 5):
            error = 'Rating is required and must be between 1 and 5.'  # Check if rating is valid

        if error is not None:
            flash(error)  # Flash an error message if validation fails
        else:
            # Insert the review into the database
            db.execute(
                'INSERT INTO review (user_id, book_id, review_text, rating) VALUES (?, ?, ?, ?)',
                (user_id, book_id, review_text, int(rating))
            )
            db.commit()  # Commit the changes
            flash('Review added successfully!')  # Flash a success message
            return redirect(url_for('books.view_book', id=book_id))  # Redirect to the book's view page

    # Pass book_title to the template along with book_id
    return render_template('review/create.html', book_id=book_id, book_title=book_title)  # Render the review creation template


@review_bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required  # Ensure the user is logged in to update a review
def update(id):
    review = get_review(id)  # Get the review details
    db = get_db()  # Get the database connection
    book = db.execute('SELECT title FROM book WHERE id = ?', (review['book_id'],)).fetchone()  # Get the book associated with the review

    if not book:
        abort(404, f"Book with ID {review['book_id']} doesn't exist.")  # Return a 404 error if the book does not exist

    if request.method == 'POST':  # Handle form submission
        review_text = request.form['review_text']  # Get the updated review text
        rating = request.form['rating']  # Get the updated rating
        error = None  # Initialize error variable

        # Validate the updated review text and rating
        if not review_text:
            error = 'Review text is required.'  # Check if review text is provided
        elif not rating or not (1 <= int(rating) <= 5):
            error = 'Rating must be between 1 and 5.'  # Check if rating is valid

        if error is not None:
            flash(error)  # Flash an error message if validation fails
        else:
            # Update the review in the database
            db.execute(
                'UPDATE review SET review_text = ?, rating = ? WHERE id = ?',
                (review_text, int(rating), id)
            )
            db.commit()  # Commit the changes
            flash('Review updated successfully!')  # Flash a success message
            return redirect(url_for('books.view_book', id=review['book_id']))  # Redirect to the book's view page

    return render_template('review/update.html', review=review, book_title=book['title'])  # Render the review update template


@review_bp.route('/<int:id>/delete', methods=('POST',))
@login_required  # Ensure the user is logged in to delete a review
def delete(id):
    review = get_review(id)  # Get the review details
    db = get_db()  # Get the database connection
    db.execute('DELETE FROM review WHERE id = ?', (id,))  # Delete the review from the database
    db.commit()  # Commit the changes
    flash('Review deleted successfully!')  # Flash a success message
    return redirect(url_for('dashboard.index'))  # Redirect to the dashboard


def get_review(id, check_author=True):
    """Retrieve a review by ID and check if the user is the author."""
    review = get_db().execute(
        'SELECT r.id, r.review_text, r.rating, r.user_id, r.book_id'
        ' FROM review r WHERE r.id = ?',
        (id,)
    ).fetchone()  # Get the review from the database

    if review is None:
        abort(404, f"Review id {id} doesn't exist.")  # Return a 404 error if the review does not exist

    if check_author and review['user_id'] != g.user['id']:
        abort(403)  # Return a 403 error if the user is not the author of the review

    return review  # Return the review details
