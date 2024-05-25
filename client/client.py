import requests
import threading
import time
import tkinter as tk
from tkinter import scrolledtext, simpledialog

SERVER_URL = 'http://localhost:8000'


class ChatClient:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Chat User: {self.username}")

        self.chat_display = scrolledtext.ScrolledText(root, state='disabled')
        self.chat_display.pack(padx=10, pady=10)

        self.message_label = tk.Label(root, text="Enter your message:")
        self.message_label.pack(padx=10, pady=5)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.get_messages_thread = threading.Thread(target=self.get_messages, daemon=True)
        self.get_messages_thread.start()

    def get_messages(self):
        while True:
            try:
                response = requests.get(f"{SERVER_URL}/api/messages")
                if response.status_code == 200:
                    messages = response.json()
                    self.chat_display.configure(state='normal', background='#a5abe3')
                    self.chat_display.delete(1.0, tk.END)
                    for message in messages:
                        self.chat_display.insert(tk.END, f"{message['username']}: {message['message']}\n")
                    self.chat_display.configure(state='disabled')
                    self.chat_display.yview(tk.END)
                else:
                    print("Failed to retrieve messages")
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(1)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            try:
                response = requests.post(f"{SERVER_URL}/api/send", json={"username": self.username, "message": message})
                if response.status_code == 200:
                    self.message_entry.delete(0, tk.END)
                else:
                    print("Failed to send message")
            except Exception as e:
                print(f"Error: {e}")


def main():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    username = simpledialog.askstring("Username", "Enter your username:", parent=root)
    ChatClient(root=root, username=username)
    root.mainloop()


if __name__ == "__main__":
    main()
