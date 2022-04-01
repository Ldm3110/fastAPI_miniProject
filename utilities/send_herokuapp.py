import requests


def send_message_to_herokuapp(message, author):
    url = "https://faulty-backend.herokuapp.com/on_comment"
    data = {
        "message": message,
        "author": author
    }

    response = requests.post(url, data=data)

    print(f"\nResponse herokuapp : {response.text}\n")
