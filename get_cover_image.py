import requests


def get_cover_image(isbn):
    """Fetch cover image URL from Google Books API using ISBN."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        book_info = data['items'][0]['volumeInfo']
        return book_info.get('imageLinks', {}).get('thumbnail', None)
    return None


def main():
    print(get_cover_image(9780618574971))


if __name__ == "__main__":
    main()