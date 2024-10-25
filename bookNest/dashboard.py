from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from bookNest.auth import login_required
from bookNest.db import get_db

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    db = get_db()
    books = db.execute('SELECT * FROM book').fetchall()
    return render_template('dashboard/index.html', books = books)


@dashboard_bp.route('/library')
@login_required
def library():
    user_id = session['user_id']
    db = get_db()
    favorites = db.execute(
        'SELECT * FROM book JOIN favorite ON book.id = favorite.book_id WHERE favorite.user_id = ?',
        (user_id,)
    ).fetchall()
    return render_template('dashboard/library.html', favorites = favorites)


@dashboard_bp.route('/review/create<int:book_id>', methods=('GET', 'POST'))
@login_required
def create_review(book_id):
    if request.method == 'POST':
        review_text = request.form['review_text']
        rating = request.form['rating']
        user_id = session['user_id']
        error = None

        if not rating:
            error = 'Rating is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO review (user_id, book_id, review_text, rating)'
                ' VALUES (?, ?, ?, ?)',
                (user_id, book_id, review_text, rating)
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('review/create.html', book_id = book_id)


def get_review(id, check_author=True):
    review = get_db().execute(
        'SELECT r.id, review_text, rating, user_id, book_id'
        ' FROM review r'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if review is None:
        abort(404, f"Review id {id} doesn't exist.")

    if check_author and review['user_id'] != g.user['id']:
        abort(403)

    return review


@dashboard_bp.route('/review/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_review(id):
    review = get_review(id)

    if request.method == 'POST':
        review_text = request.form['review_text']
        rating = request.form['rating']
        error = None

        if not rating:
            error = 'Rating is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE review SET review_text = ?, rating = ?'
                ' WHERE id = ?',
                (review_text, rating, id)
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('review/update.html', review = review)


@dashboard_bp.route('/review/<int:id>/delete', methods=('POST',))
@login_required
def delete_review(id):
    get_review(id)
    db = get_db()
    db.execute('DELETE FROM review WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard.index'))