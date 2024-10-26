from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from bookNest.auth import login_required
from bookNest.db import get_db

review_bp = Blueprint('review', __name__, url_prefix='/review')


@review_bp.route('/create/<int:book_id>', methods=('GET', 'POST'))
@login_required
def create(book_id):
    db = get_db()
    # Retrieve the book title based on the book_id
    book = db.execute('SELECT title FROM book WHERE id = ?', (book_id,)).fetchone()

    # Check if the book exists
    if book is None:
        abort(404, f"Book with ID {book_id} does not exist.")

    book_title = book['title']  # Extract the book title from the query result

    if request.method == 'POST':
        review_text = request.form['review_text']
        rating = request.form['rating']
        user_id = session.get('user_id')
        error = None

        if not review_text:
            error = 'Review text is required.'
        elif not rating or not (1 <= int(rating) <= 5):
            error = 'Rating is required and must be between 1 and 5.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO review (user_id, book_id, review_text, rating) VALUES (?, ?, ?, ?)',
                (user_id, book_id, review_text, int(rating))
            )
            db.commit()
            flash('Review added successfully!')
            return redirect(url_for('books.view_book', id=book_id))

    # Pass book_title to the template along with book_id
    return render_template('review/create.html', book_id=book_id, book_title=book_title)


@review_bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    review = get_review(id)
    db = get_db()
    book = db.execute('SELECT title FROM book WHERE id = ?', (review['book_id'],)).fetchone()

    if not book:
        abort(404, f"Book with ID {review['book_id']} doesn't exist.")

    if request.method == 'POST':
        review_text = request.form['review_text']
        rating = request.form['rating']
        error = None

        if not review_text:
            error = 'Review text is required.'
        elif not rating or not (1 <= int(rating) <= 5):
            error = 'Rating must be between 1 and 5.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE review SET review_text = ?, rating = ? WHERE id = ?',
                (review_text, int(rating), id)
            )
            db.commit()
            flash('Review updated successfully!')
            return redirect(url_for('books.view_book', id=review['book_id']))

    return render_template('review/update.html', review=review, book_title=book['title'])


@review_bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    review = get_review(id)
    db = get_db()
    db.execute('DELETE FROM review WHERE id = ?', (id,))
    db.commit()
    flash('Review deleted successfully!')
    return redirect(url_for('dashboard.index'))


def get_review(id, check_author=True):
    review = get_db().execute(
        'SELECT r.id, r.review_text, r.rating, r.user_id, r.book_id'
        ' FROM review r WHERE r.id = ?',
        (id,)
    ).fetchone()

    if review is None:
        abort(404, f"Review id {id} doesn't exist.")

    if check_author and review['user_id'] != g.user['id']:
        abort(403)

    return review
