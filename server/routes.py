from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body, HTTPException
from starlette import status

from models import MessageRequest, ChatRoom, User
from database import get_messages, add_message, add_room, get_rooms, get_user, create_user
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
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[room_name].remove(websocket)


async def notify_clients(room_name: str, message: MessageRequest):
    for websocket in active_connections[room_name]:
        await websocket.send_json({"username": message.username, "message": message.message})


@router.post("/api/login")
async def login(username: str = Body(...), password: str = Body(...)):
    user = await get_user(username)
    if user and user['password'] == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


@router.post("/api/signup")
async def sign_up(username: str = Body(...), password: str = Body(...)):
    new_user = User(username=username, password=password)
    user_in_db = await get_user(new_user.username)
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    await create_user(user=new_user)
    return {"message": "User registered successfully"}

