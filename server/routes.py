from fastapi import APIRouter
from models import MessageRequest, ChatRoom
from database import get_messages, add_message, add_room, get_rooms

router = APIRouter()


@router.post("/api/send/{room_name}")
async def send_message(room_name: str, message: MessageRequest):
    await add_message(room_name, message)
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
