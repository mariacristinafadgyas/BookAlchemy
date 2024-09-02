from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

db = SQLAlchemy()  # Creates a db object


class Author(db.Model):
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(String(100))
    date_of_death = db.Column(String(100))

    def __repr__(self):
        return f"Author: {self.name} (id = {self.id})"


class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.author_id'))
    isbn = db.Column(db.String(30))
    title = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)

    def __repr__(self):
        return f"Book title: {self.title}, {self.publication_year}"
