# My Library

This is a web-based Book Library Management System built using Flask and SQLAlchemy. It allows users to manage books and authors, including adding, deleting, and viewing details. Additionally, it includes functionality for customizing the UI appearance and providing book suggestions.

## Features

- **Book Management**
  - Add new books to the library.
  - View detailed information about a specific book.
  - Delete books from the library.

- **Author Management**
  - Add new authors to the library.
  - Delete authors, including handling the deletion of authors with no remaining books.

- **Search and Sort**
  - Search for books and authors using a search query.
  - Sort books by title, author, or publication year in ascending or descending order.

- **User Interface Customization**
  - Customize the website's color theme using a color picker.

- **Book Suggestions**
  - Get book suggestions based on a randomly selected book from the library.

## Installation

1. Clone the repository :
```
git clone https://github.com/mariacristinafadgyas/BookAlchemy
```
2. Navigate to the project directory:
```
cd BookAlchemy
```
3. Create a virtual environment and activate it:
```
python -m venv venv
```
```
source venv/bin/activate
```
4. Install the required packages:
```
pip install -r requirements.txt
```
5. Set up the database:
```
flask db upgrade
```
6. Run the Flask app
```
python app.py
```
## Endpoints
### Home
- URL: **/**
- Method: **GET**
- Description: Displays the home page with options to search and sort books.
### Add Book
- URL: **/add_book**
- Method: **GET, POST**
- Description: Form for adding new books. Handles validation and error messages.
###Add Author
- URL: **/add_author**
- Method: **GET, POST**
- Description: Form for adding new authors. Includes validation for dates.
### Book Details
- URL: **/book/<int:book_id>**
- Method: **GET**
- Description: Displays details for a specific book identified by book_id.
### Author Details
- URL: **/author/<int:author_id>**
- Method: **GET**
- Description: Displays details for a specific author and their books.
### Delete Book
- URL: **/book/<int:book_id>/delete**
- Method: **POST**
- Description: Deletes a specific book. If the book was the only one by its author, the author is also deleted.
### Delete Author
- URL: **/author/<int:author_id>/delete**
- Method: **POST**
- Description: Deletes a specific author. Shows an error message if the author does not exist.
### Suggest Book
- URL: **/suggest_book**
- Method: **GET**
- Description: Provides a suggestion for a book from the library.
### Customization
- **Color Picker**: Allows users to select a color theme for the website. The color value is stored in local storage and applied dynamically.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.