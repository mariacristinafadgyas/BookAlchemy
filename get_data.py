from dotenv import load_dotenv
import os
import requests


load_dotenv()
gpt_key = os.getenv('gpt_key')

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


def get_suggestion(title):
    # First API - It is very slow
    # url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4-2"
    #
    # question_content = (f"Please write a short suggestion for this {title} as to why"
    #                     f" I should read this book. The suggestion should be no longer"
    #                     f" than 3 or 4 sentences.")
    # payload = {
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": question_content,
    #         }
    #     ],
    #     "system_prompt": "",
    #     "temperature": 0.9,
    #     "top_k": 5,
    #     "top_p": 0.9,
    #     "max_tokens": 256,
    #     "web_access": False
    # }
    # headers = {
    #     "x-rapidapi-key": '29e4910dcbmsh8f620cdeb08c4b4p1bca49jsndd4e2fb86c75',
    #     "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    #     "Content-Type": "application/json"
    # }
    # try:
    #     response = requests.post(url, json=payload, headers=headers)
    #     response.raise_for_status()
    #     response_data = response.json()
    #
    #     if not response_data.get('status', True):
    #         return 'No suggestion available at the moment. Please try again later.'
    #
    #     return response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No suggestion available.')
    #
    # except requests.RequestException as e:
    #     print(f"An error occurred: {e}")
    #     return 'No suggestion available due to an error. Please try again later.'

    # Second API
    url = "https://chat-gpt26.p.rapidapi.com/"

    question_content = (f"Please write a short suggestion for this {title} as to why"
                        f" I should read this book. The suggestion should be no longer"
                        f" than 3 or 4 sentences.")
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": question_content
            }
        ]
    }
    headers = {
        "x-rapidapi-key": gpt_key,
        "x-rapidapi-host": "chat-gpt26.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        choices = response_data.get('choices', [])
        if not choices:
            return 'No suggestion available at the moment. Please try again later.'

        suggestion = choices[0].get('message', {}).get('content', 'No suggestion available.')
        return suggestion

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return 'No suggestion available due to an error. Please try again later.'


def main():
    print(get_cover_image(9780553103540))
    print(get_description(9780553103540))
    print(get_rating(9780553103540))
    print(get_suggestion('A Tale of Two Cities'))


if __name__ == "__main__":
    main()