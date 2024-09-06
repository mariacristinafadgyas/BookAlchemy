from data_models import db, Author, Book
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from get_data import *
import os
import random
from sqlalchemy import func

load_dotenv()
flash_key = os.getenv('flash_key')

app = Flask(__name__)
app.secret_key = flash_key

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "data", "library.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Connects the Flask app to the flask-sqlalchemy code

migrate = Migrate(app, db)

# # Creates the tables defined in the models
# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
    """Renders the homepage of the library application, displaying a list of
    books with sorting and search functionalities. retrieves books from the
    database, allowing users to sort the results by title, author, or publication
    year. Users can also search for books or authors by entering a query. Renders
    the 'home.html' template with the list of books, including sorting and search
    parameters."""

    sort_by = request.args.get('sort_by', 'title')  # Default to sorting by title
    sort_order = request.args.get('sort_order', 'asc')  # Default to ascending order
    search_query = request.args.get('search_query', '').strip()

    if search_query:
        books = Book.query.join(Author).filter(
            (Book.title.ilike(f'%{search_query}%')) |
            (Author.name.ilike(f'%{search_query}%'))
        ).all()
        if not books:
            flash('No books or authors match your search criteria.')
    else:
        # Map sorting field to model attribute
        sort_field = {
            'title': Book.title,
            'author': Author.name,
            'publication_year': Book.publication_year
        }.get(sort_by, Book.title)

        # Determine the sort direction
        if sort_order == 'desc':
            books = Book.query.join(Author).order_by(sort_field.desc()).all()
        else:
            books = Book.query.join(Author).order_by(sort_field).all()

    return render_template('home.html', books=books, sort_by=sort_by, sort_order=sort_order, search_query=search_query)


@app.route('/add_author', methods=['GET', 'POST'])
def add_authors():
    """ Handles the addition of new authors to the library database. For a GET request,
    this function outputs the ‘add_authors’ form for user input.When a
    POST request is made, the form is processed to add a new author with
    details such as name, date of birth and date of death."""

    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        # Server-side date format validation and conversion
        date_format = "%Y-%m-%d"
        birth_date = None
        date_of_death = None

        try:
            if birth_date_str:  # Validate the birthdate
                birth_date = datetime.strptime(birth_date_str, date_format).date()
            else:
                None
            if date_of_death_str:  # Validate the date of death
                date_of_death = datetime.strptime(date_of_death_str, date_format).date()
            else:
                None

        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.")
            return redirect(url_for('add_authors'))

        if birth_date and date_of_death and date_of_death < birth_date:
            flash("The date of death cannot be earlier than the birth date.")
            return redirect(url_for('add_authors'))

        existing_author = Author.query.filter(func.lower(Author.name) == func.lower(name)).first()
        if existing_author:
            flash('An author with this name already exists.')
            return redirect(url_for('add_authors'))

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        # Add to the session and commit to the database
        db.session.add(new_author)
        db.session.commit()

        flash(f'{new_author} successfully added!')  # Flash success message

        return redirect(url_for('add_authors'))
    return render_template('add_authors.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_books():
    """Handles the addition of new books to the library database. For a GET request,
     this function renders the form ‘add_books'.When a POST request is made, it
     processes the form submission to add a new book with details such as title,
     ISBN, year of publication and author, and the cover image, description and
     rating of the book are retrieved from an API."""

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

        existing_book = Book.query.filter(func.lower(Book.title) == func.lower(title)).first()
        if existing_book:
            flash('A book with this title already exists. Please choose a different title.')
            return redirect(url_for('add_books'))

        try:
            publication_year = int(publication_year)
            current_year = datetime.now().year
            if publication_year < 1000 or publication_year > current_year:
                raise ValueError('Invalid publication year!')
        except ValueError:
            flash('Please enter a valid publication year between 1000 and the current year.')
            return redirect(url_for('add_books'))

        # Fetch the selected author from the database
        author = Author.query.get(author_id)
        if not author:
            flash('Selected author does not exist.')
            return redirect(url_for('add_books'))

        # Fetch the cover image URL and description using the ISBN
        cover_image = get_cover_image(isbn)
        if cover_image is None:
            cover_image = url_for('static', filename='book.jpeg')

        description = get_description(isbn)
        if description is None:
            description = 'Description currently unavailable'

        rating = get_rating(isbn)
        if rating is None:
            rating = 0.0

        purchase_link = get_link_to_buy(isbn)
        if purchase_link is None:
            purchase_link = 'Not available'

        new_book = Book(
            title=title,
            author=author,
            isbn=isbn,
            publication_year=publication_year,
            cover_image=cover_image,
            description=description,
            rating=rating,
            purchase_link = purchase_link
        )

        db.session.add(new_book)
        db.session.commit()

        flash(f'{new_book}, successfully added!')
        return redirect(url_for('add_books'))

    authors = Author.query.all()  # Fetch all authors from the database
    return render_template('add_books.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Deletes a specific book and its associated author if the book is the
     author's only entry in the library. Returns a redirect to the home page
      after the deletion."""
    book = Book.query.get_or_404(book_id)
    author = book.author
    print(author)

    try:
        db.session.delete(book)
        db.session.commit()

        author_books_count = Book.query.filter_by(author_id=author.author_id).count()

        if author_books_count == 0:
            db.session.delete(author)
            db.session.commit()
            flash(f"As the book ‘{book.title}’ was the only book in our library,"
                  f" its author ‘{author.name}’ was also successfully deleted.")
        else:
            flash(f'The book "{book.title}" has been successfully deleted.')

    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while trying to delete the book: {str(e)}', 'danger')

    return redirect(url_for('home'))


@app.route('/author/<int:author_id>')
def author_details(author_id):
    """Displays the details of a specific author and their associated books
     and returns a rendered template of 'author_details.html' with the
      author's details and their books."""

    author = Author.query.get_or_404(author_id)
    books = Book.query.filter_by(author_id=author_id).all()

    return render_template('author_details.html', author=author, books=books)


@app.route('/book/<int:book_id>', methods=['GET'])
def book_details(book_id):
    """Displays the details of a specific book and returns a rendered
     template of 'book_details.html' with the book's details"""

    book = Book.query.get_or_404(book_id)

    return render_template('book_details.html', book=book)


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    """Deletes an author and all associated books from the database. Returns a
     redirect response to the 'home' route."""

    author = Author.query.get(author_id)

    if author is None:
        flash('Author not found!')
        return redirect(url_for('home'))

    try:
        db.session.delete(author)
        db.session.commit()
        flash('Author and all associated books successfully deleted!')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the author and associated books. Please try again.')

    return redirect(url_for('home'))


@app.route('/suggest_book', methods=['GET'])
def suggest_book():
    """Suggests a book to the user by randomly selecting one from the database
     and returns a rendered template of 'suggest_book.html' with the selected
      book details and suggestion. Redirects to 'home' if no books are available."""

    titles = Book.query.all()
    if not titles:
        flash('No books available for suggestion.')
        return redirect(url_for('home'))

    title = random.choice(titles).title
    suggestion_response = get_suggestion(title)

    book = Book.query.filter_by(title=title).first_or_404()

    return render_template('suggest_book.html', book=book, suggestion=suggestion_response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
