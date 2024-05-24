import requests
import threading
import time
import os


SERVER_URL = 'http://localhost:8000'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_messages():
    while True:
        try:
            response = requests.get(f"{SERVER_URL}/api/messages")
            if response.status_code == 200:
                messages = response.json()
                clear_screen()
                for message in messages:
                    print(f"{message['username']}: {message['message']}")
            else:
                print("Failed to retrieve messages")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(10)


def send_message(username):
    while True:
        message = input()
        try:
            response = requests.post(f"{SERVER_URL}/api/send", json={"username": username, "message": message})
            if response.status_code != 200:
                print("Failed to send message")
        except Exception as e:
            print(f"Error: {e}")


def main():
    username = input("Enter your username: ")
    threading.Thread(target=get_messages, daemon=True).start()
    send_message(username)


if __name__ == "__main__":
    main()
