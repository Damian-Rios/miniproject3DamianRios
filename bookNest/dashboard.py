from flask import (
    Blueprint, flash, render_template, request
)
from bookNest.auth import login_required
from bookNest.db import get_db

# Create a Blueprint for the dashboard functionality
dashboard_bp = Blueprint('dashboard', __name__)

# Route to display the dashboard with books
@dashboard_bp.route('/')
@login_required  # Ensure the user is logged in before accessing this route
def index():
    db = get_db()  # Get the database connection
    genre = request.args.get('genre')  # Get the selected genre from query parameters
    sort_by_rating = request.args.get('sort_by_rating')  # Get the sort option from query parameters

    # Construct the base SQL query to retrieve books and their average ratings
    query = '''
        SELECT b.id, b.title, b.author, b.genre, b.description, b.user_id,
               COALESCE(AVG(r.rating), 0) AS avg_rating
        FROM book b
        LEFT JOIN review r ON b.id = r.book_id
    '''
    params = []  # List to hold parameters for the query

    # Add a filter for the selected genre if provided
    if genre:
        query += ' WHERE b.genre = ?'
        params.append(genre)  # Add the genre to the parameters

    # Group the results by book ID to calculate the average rating
    query += ' GROUP BY b.id'

    # Add sorting options based on the user's selection
    if sort_by_rating == 'desc':
        query += ' ORDER BY avg_rating DESC'  # Sort by average rating in descending order
    elif sort_by_rating == 'asc':
        query += ' ORDER BY avg_rating ASC'  # Sort by average rating in ascending order

    # Execute the query and fetch all results
    books = db.execute(query, params).fetchall()

    # Check if any books were found; if not, flash a message
    if not books:
        flash('No books found. Add some books to get started!')

    # Render the dashboard template with the retrieved books
    return render_template('dashboard/index.html', books=books)
