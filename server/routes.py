from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from models import MessageRequest, ChatRoom
from database import get_messages, add_message, add_room, get_rooms
from typing import List
from collections import defaultdict

router = APIRouter()
active_connections: defaultdict[str, List[WebSocket]] = defaultdict(list)

@router.post("/api/send/{room_name}")
async def send_message(room_name: str, message: MessageRequest):
    await add_message(room_name, message)
    await notify_clients(room_name, message)
    return {"message": "Message sent successfully"}

@router.get("/api/messages/{room_name}")
async def get_all_messages(room_name: str):
    messages = await get_messages(room_name=room_name)
    return messages

@router.post("/api/rooms")
async def create_room(room: ChatRoom):
    await add_room(room=room)
    return {"room": "Room created successfully"}

@router.get("/api/rooms")
async def get_all_rooms():
    rooms = await get_rooms()
    return rooms

@router.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await websocket.accept()
    active_connections[room_name].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any received messages from the client if necessary
    except WebSocketDisconnect:
        active_connections[room_name].remove(websocket)

async def notify_clients(room_name: str, message: MessageRequest):
    for websocket in active_connections[room_name]:
        await websocket.send_json({"username": message.username, "message": message.message})
