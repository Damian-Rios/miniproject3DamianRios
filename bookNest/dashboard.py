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
    sort_by_rating = request.args.get('sort_by_rating')

    # Construct base query
    query = '''
        SELECT b.id, b.title, b.author, b.genre, b.description, b.user_id,
               COALESCE(AVG(r.rating), 0) AS avg_rating
        FROM book b
        LEFT JOIN review r ON b.id = r.book_id
    '''
    params = []

    # Add genre filter if selected
    if genre:
        query += ' WHERE b.genre = ?'
        params.append(genre)

    # Group by book ID for avg_rating calculation
    query += ' GROUP BY b.id'

    # Add sorting by rating if selected
    if sort_by_rating == 'desc':
        query += ' ORDER BY avg_rating DESC'
    elif sort_by_rating == 'asc':
        query += ' ORDER BY avg_rating ASC'

    books = db.execute(query, params).fetchall()

    if not books:
        flash('No books found. Add some books to get started!')

    return render_template('dashboard/index.html', books=books)
