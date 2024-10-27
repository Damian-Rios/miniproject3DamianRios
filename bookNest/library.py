from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .db import get_db
from flask import g

library_bp = Blueprint('library', __name__, url_prefix='/library')


@library_bp.route('/')
def library():
    user_id = session.get('user_id')
    db = get_db()
    books = db.execute(
        'SELECT b.*, l.favorite, l.status FROM library l '
        'JOIN book b ON l.book_id = b.id '
        'WHERE l.user_id = ?',
        (user_id,)
    ).fetchall()
    return render_template('library/library.html', books=books)


@library_bp.route('/add/<int:book_id>', methods=['GET', 'POST'])
def add_to_library(book_id):
    user_id = session.get('user_id')
    db = get_db()
    existing_entry = db.execute(
        'SELECT * FROM library WHERE user_id = ? AND book_id = ?',
        (user_id, book_id)
    ).fetchone()

    if existing_entry is None:
        db.execute(
            'INSERT INTO library (user_id, book_id) VALUES (?, ?)',
            (user_id, book_id)
        )
        db.commit()
        flash('Book added to your library!', 'success')
    else:
        flash('Book is already in your library!', 'info')

    return redirect(url_for('books.view_book', id=book_id))


@library_bp.route('/update_status/<int:book_id>', methods=['POST'])
def update_status(book_id):
    user_id = session.get('user_id')
    status = request.form['status']
    db = get_db()
    db.execute(
        'UPDATE library SET status = ? WHERE user_id = ? AND book_id = ?',
        (status, user_id, book_id)
    )
    db.commit()
    flash('Status updated successfully!', 'success')
    return redirect(url_for('library.library'))


@library_bp.route('/remove/<int:book_id>', methods=['POST'])
def remove_from_library(book_id):
    user_id = session.get('user_id')
    db = get_db()
    db.execute(
        'DELETE FROM library WHERE user_id = ? AND book_id = ?',
        (user_id, book_id)
    )
    db.commit()
    flash('Book removed from your library.', 'success')
    return redirect(url_for('library.library'))
