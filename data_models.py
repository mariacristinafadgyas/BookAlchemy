from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Creates a db object


class Author(db.Model):
    """Defines the structure of the 'authors' table in the database,
    with attributes corresponding to the author"""
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Author: {self.name} "


class Book(db.Model):
    """Defines the structure of the 'books' table in the database,
       with attributes corresponding to the book"""
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)
    isbn = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    purchase_link = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Book: {self.title}, published in {self.publication_year}"
