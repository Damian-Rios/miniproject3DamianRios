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


@books_bp.route('/view/<int:id>')
def view_book(id):
    db = get_db()

    # Get the book
    book = db.execute('SELECT * FROM book WHERE id = ?', (id,)).fetchone()

    if book is None:
        flash('Book not found.')
        return redirect(url_for('dashboard.index'))  # Redirect if book not found

    # Get reviews along with usernames
    reviews = db.execute('SELECT r.*, u.username FROM review r JOIN user u ON r.user_id = u.id WHERE r.book_id = ?',
                         (id,)).fetchall()

    # Get the average rating
    avg_rating_row = db.execute('SELECT COALESCE(AVG(r.rating), 0) AS avg_rating FROM review r WHERE r.book_id = ?',
                                (id,)).fetchone()

    # Check if avg_rating_row is valid and convert to float if necessary
    avg_rating = avg_rating_row['avg_rating'] if avg_rating_row else 0.0
    try:
        avg_rating = round(float(avg_rating), 1)  # Round to one decimal place
    except TypeError:
        avg_rating = 0.0  # Default to 0 if rounding fails

    return render_template('books/viewBook.html', book=book, reviews=reviews, avg_rating=avg_rating)


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

