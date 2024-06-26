import json
import logging

import requests
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, ttk
import asyncio
import websockets

SERVER_URL = 'http://localhost:8000'


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.room = None
        self.options_box = None
        self.chat_display = None
        self.message_entry = None

        self.login_or_signup()

    def login_or_signup(self):
        choice = messagebox.askyesno("Login or Signup", "Do you want to login?")
        if choice:
            self.login()
        else:
            self.signup()

    def login(self):
        username = simpledialog.askstring("Login", "Enter your username:", parent=self.root)
        password = simpledialog.askstring("Login", "Enter your password:", parent=self.root, show="*")
        try:
            response = requests.post(f"{SERVER_URL}/api/login", json={"username": username, "password": password})
            if response.status_code == 200:
                self.username = username
                self.create_chat_interface()
            else:
                messagebox.showerror("Error", "Invalid username or password. Please try again.")
        except Exception as e:
            print(f"Error: {e}")

    def signup(self):
        username = simpledialog.askstring("Signup", "Enter your username:", parent=self.root)
        password = simpledialog.askstring("Signup", "Enter your password:", parent=self.root, show="*")
        try:
            response = requests.post(f"{SERVER_URL}/api/signup", json={"username": username, "password": password})
            if response.status_code == 200:
                self.username = username
                self.create_chat_interface()
            else:
                messagebox.showerror("Error", "Failed to signup. Username might already exist.")
        except Exception as e:
            print(f"Error: {e}")

    def create_chat_interface(self):
        self.root.title(f"Chat User: {self.username}")
        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled')
        self.chat_display.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

        self.choose_room()

    def choose_room(self):
        rooms = requests.get(f"{SERVER_URL}/api/rooms").json()
        if rooms:
            rooms_options = [room['name'] for room in rooms]
            self.options_box = ttk.Combobox(
                state="readonly",
                values=rooms_options
            )
            self.options_box.place(x=50, y=50)
            button = ttk.Button(text="Select Room", command=self.display_selection)
            button.place(x=50, y=100)
        else:
            messagebox.showinfo("Info", "No rooms available. Please create a room first.")
            self.create_room()

    def display_selection(self):
        self.room = self.options_box.get()
        self.root.title(f"Chat User: {self.username} | Room: {self.room if self.room else ''}")
        messagebox.showinfo(
            message=f"The selected Room is: {self.room}",
            title="Selection"
        )
        threading.Thread(target=self.websocket_listener, daemon=True).start()

    def create_room(self):
        room_name = simpledialog.askstring("Create Room", "Enter room name:", parent=self.root)
        if room_name:
            try:
                response = requests.post(f"{SERVER_URL}/api/rooms", json={"name": room_name})
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Room created successfully.")
                    self.room = room_name
                else:
                    messagebox.showerror("Error", "Failed to create room.")
            except Exception as e:
                print(f"Error: {e}")

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            try:
                response = requests.post(f"{SERVER_URL}/api/send/{self.room}", json={"username": self.username,
                                                                                     "message": message})
                if response.status_code == 200:
                    self.message_entry.delete(0, tk.END)
                    self.notify_users_seen_message()
                else:
                    print("Failed to send message")
            except Exception as e:
                print(f"Error: {e}")

    def notify_users_seen_message(self):
        try:
            response = requests.get(f"{SERVER_URL}/api/users/{self.room}")
            if response.status_code == 200:
                users = response.json()
                seen_by_users = ', '.join(users)
                logging.info(f"Users {seen_by_users} have seen your message")
        except Exception as e:
            print(f"Error: {e}")

    def websocket_listener(self):
        async def listen():
            uri = f"ws://localhost:8000/ws/{self.room}"
            try:
                async with websockets.connect(uri) as websocket:
                    while True:
                        data = await websocket.recv()
                        message = json.loads(data)
                        self.chat_display.configure(state='normal', background='#a5abe3')
                        self.chat_display.insert(tk.END, f"{message['username']}: {message['message']}\n")
                        self.chat_display.configure(state='disabled')
                        self.chat_display.yview(tk.END)
            except Exception as e:
                print(f"WebSocket Error: {e}")

        asyncio.new_event_loop().run_until_complete(listen())


def main():
    root = tk.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    ChatClient(root=root)
    root.mainloop()


if __name__ == "__main__":
    main()
