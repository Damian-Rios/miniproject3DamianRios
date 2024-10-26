from flask import Blueprint, g, render_template, request, redirect, url_for, flash
from .db import get_db

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']
        user_id = g.user['id']

        if not title or not author or not genre or not description:
            flash('All fields are required!')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO book (title, author, genre, description, user_id) VALUES (?, ?, ?, ?, ?)',
                (title, author, genre, description, user_id)
            )
            db.commit()
            flash('Book added successfully!')
            return redirect(url_for('dashboard.index'))

    return render_template('books/addBook.html')


@books_bp.route('/delete/<int:id>', methods=('POST',))
def delete_book(id):
    db = get_db()
    db.execute('DELETE FROM book WHERE id = ?', (id,))
    db.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('dashboard.index'))


@books_bp.route('/update/<int:id>', methods=('GET', 'POST'))
def update_book(id):
    db = get_db()
    book = db.execute('SELECT * FROM book WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']  # Added description

        if not title or not author or not genre or not description:
            flash('All fields are required!')
        else:
            db.execute(
                'UPDATE book SET title = ?, author = ?, genre = ?, description = ? WHERE id = ?',
                (title, author, genre, description, id)
            )
            db.commit()
            flash('Book updated successfully!')
            return redirect(url_for('dashboard.index'))

    return render_template('books/updateBook.html', book=book)

