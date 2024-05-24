import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_send_message():
    response = client.post("/api/send", json={"username": "testuser", "message": "Hello friends"})
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent successfully"}


def test_send_and_get_messages():
    client.post("/api/send", json={"username": "testuser", "message": "Hello friends"})
    response = client.get("/api/messages")
    assert response.status_code == 200
    assert response.json()[0] == {"username": "testuser", "message": "Hello friends"}


def test_send_messages_invalid_data():
    response = client.post("/api/send", json={"username": 5, "message": "Hello friends"})
    assert response.json()['detail'][0]['msg'] == 'Input should be a valid string'
