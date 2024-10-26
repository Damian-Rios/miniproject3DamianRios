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
    genre = request.args.get('genre')

    # Fetch books based on genre
    if genre:
        books = db.execute('''
            SELECT b.id, b.title, b.author, b.genre, b.description, b.user_id,
                   COALESCE(AVG(r.rating), 0) AS avg_rating
            FROM book b
            LEFT JOIN review r ON b.id = r.book_id
            WHERE b.genre = ?
            GROUP BY b.id
        ''', (genre,)).fetchall()
    else:
        books = db.execute('''
            SELECT b.id, b.title, b.author, b.genre, b.description, b.user_id,
                   COALESCE(AVG(r.rating), 0) AS avg_rating
            FROM book b
            LEFT JOIN review r ON b.id = r.book_id
            GROUP BY b.id
        ''').fetchall()

    # If no books are found, you could consider flashing a message or handling it in the template
    if not books:
        flash('No books found. Add some books to get started!')

    return render_template('dashboard/index.html', books=books)


@dashboard_bp.route('/library')
@login_required
def library():
    user_id = session['user_id']
    db = get_db()
    favorites = db.execute(
        'SELECT * FROM book JOIN favorite ON book.id = favorite.book_id WHERE favorite.user_id = ?',
        (user_id,)
    ).fetchall()
    return render_template('dashboard/library.html', favorites=favorites)
