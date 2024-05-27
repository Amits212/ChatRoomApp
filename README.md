# ChatRoomApp

ChatRoomApp is a simple chat application that allows users to sign up, log in, join chat rooms, and send messages. The backend is built with FastAPI and MongoDB, and the frontend is implemented using Tkinter.

## Features

- User authentication (signup and login)
- Create and join chat rooms
- Send and receive messages in real-time
- See the list of users in the same chat room

## Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Docker Compose

### Backend Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Amits212/ChatRoomApp.git
    cd ChatRoomApp
    ```

2. **Start the backend services:**

    Use Docker Compose to build and start the backend services (FastAPI and MongoDB).

    docker-compose up --build

    This command will start the FastAPI server on `http://localhost:8000`.

### Client Setup

The client application is built with Tkinter and needs to be run separately since it hasn't been containerized.

1. **Run the client application:**

    python ./client/client.py

    This command will start the Tkinter-based client application.

## API Endpoints

### User Authentication

- **Signup**

    POST /api/signup

    Request body:


    {
        "username": "your-username",
        "password": "your-password"
    }

- **Login**

    POST /api/login

    Request body:

    {
        "username": "your-username",
        "password": "your-password"
    }

### Chat Rooms

- **Create a new room**

    POST /api/rooms

    Request body:

    {
        "name": "room-name"
    }

- **Get all rooms**

    GET /api/rooms

- **Get all messages in a room**

    
    GET /api/messages/{room_name}

- **Send a message**

    POST /api/send/{room_name}

    Request body:

    {
        "username": "your-username",
        "message": "your-message"
    }

- **Get users in a room**

    GET /api/users/{room_name}


Directory Structure:

ChatRoomApp/
├── client/
│   └── client.py
├── server/
│   ├── app.py
│   ├── routes.py
│   ├── models.py
│   ├── database.py
├   |── test_apis.py
│   └── Dockerfile
├── docker-compose.yml
└── README.md

