from data_models import db, Author, Book
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
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


@app.route('/add_author', methods=['GET', 'POST'])
def add_authors():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        # Server-side date format validation and conversion
        date_format = "%Y-%m-%d"
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

        new_book = Book(title=title, author=author, isbn=isbn, publication_year=publication_year)

        db.session.add(new_book)
        db.session.commit()

        flash(f'{new_book}, successfully added!')
        return redirect(url_for('add_books'))

    authors = Author.query.all()  # Fetch all authors from the database
    return render_template('add_books.html', authors=authors)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
