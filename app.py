from data_models import db, Author, Book
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from get_cover_image import get_cover_image
import os


load_dotenv()
flash_key = os.getenv('flash_key')

app = Flask(__name__)
app.secret_key = flash_key

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "data", "library.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) # Connects the Flask app to the flask-sqlalchemy code

migrate = Migrate(app, db)

# # Creates the tables defined in the models
# with app.app_context():
#     db.create_all()


@app.route('/')
def home():
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
            if date_of_death_str: # Validate the date of death
                date_of_death = datetime.strptime(date_of_death_str, date_format).date()
            else:
                None

        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.")
            return redirect(url_for('add_authors'))

        if birth_date and date_of_death and date_of_death < birth_date:
            flash("The date of death cannot be earlier than the birth date.")
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
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')

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

        # Fetch the cover image URL using the ISBN
        cover_image = get_cover_image(isbn)
        if cover_image is None:
            cover_image = url_for('static', filename='book.jpeg')

        new_book = Book(title=title, author=author, isbn=isbn, publication_year=publication_year, cover_image=cover_image)

        db.session.add(new_book)
        db.session.commit()

        flash(f'{new_book}, successfully added!')
        return redirect(url_for('add_books'))

    authors = Author.query.all()  # Fetch all authors from the database
    return render_template('add_books.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
