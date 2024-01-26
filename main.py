# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

# Create the database and tables
def addcontext():
    with app.app_context():
        db.create_all()

# Route to display list of books
@app.route('/books')
def books():
    book_list = Book.query.all()
    return render_template('books.html', books=book_list)

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        # Create a new book
        new_book = Book(title=title, author=author, publication_year=publication_year)

        # Add the book to the database
        db.session.add(new_book)
        db.session.commit()

        # Redirect to the books page
        return redirect(url_for('books'))

    return render_template('add_book.html')

# Run the app
if __name__ == '__main__':
    addcontext()  # Create the database before running the app
    app.run(debug=True)
