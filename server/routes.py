from fastapi import APIRouter, HTTPException
from models import MessageRequest
from database import get_messages, add_message
from fastapi import Response

router = APIRouter()

@router.post("/api/send")
async def send_message(message: MessageRequest):
    add_message(message)
    return {"message": "Message sent successfully"}

@router.get("/api/messages")
async def get_all_messages():
    return get_messages()
