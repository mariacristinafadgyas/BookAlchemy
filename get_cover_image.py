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


def get_description(isbn):
    """Fetch description from Google Books API using ISBN."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            for index in [0, 1]:
                try:
                    book_info = data['items'][index]['volumeInfo']
                    description = book_info.get('description')
                    if description:
                        return description
                except (IndexError, KeyError, TypeError):
                    continue
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data from the API: {e}")
    return None


def get_rating(isbn):
    """Fetch average rating from Google Books API using ISBN."""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            for index in [0, 1]:
                try:
                    book_info = data['items'][index]['volumeInfo']
                    rating = book_info.get('averageRating')
                    if rating:
                        return rating
                except (IndexError, KeyError, TypeError):
                    continue
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data from the API: {e}")
    return None


def main():
    print(get_cover_image(9780553103540))
    print(get_description(9780553103540))
    print(get_rating(9780553103540))


if __name__ == "__main__":
    main()