from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'    # creation of SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Book(db.Model):                               # creating a book model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)


def addcontext():                           # This function creates the database content and tables
    with app.app_context():
        db.create_all()

# This code routes to display list of books
@app.route('/books')
def books():
    book_list = Book.query.all()
    return render_template('books.html', books=book_list)

@app.route('/add_book', methods=['GET', 'POST'])    #  This is route for adding a new book
def add_book():
    if request.method == 'POST':
        # Get data from the form
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        new_book = Book(title=title, author=author, publication_year=publication_year)

        # This adds the book to the database
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))

    return render_template('add_book.html')

# This is runs the app
if __name__ == '__main__':
    addcontext()
    app.run(debug=True)
