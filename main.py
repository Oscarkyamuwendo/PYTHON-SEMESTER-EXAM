from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

                                # first Flask app is ceated
app = Flask(__name__)

                                        # initiated for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

                                    # Initializing     SQLAlchemy
db = SQLAlchemy(app)

                                                # this code creates a book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

                                            # Created the database and tables
def addcontext():
    with app.app_context():
        db.create_all()

@app.route('/books')                
                                                # This routes to display list of books
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
        new_book = Book(title=title, author=author, publication_year=publication_year)

        # Adding the book to the database
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))

    return render_template('add_book.html')

if __name__ == '__main__':
    addcontext()                                  # this code runs the app
    app.run(debug=True)
