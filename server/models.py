from typing import List

from pydantic import BaseModel


class MessageRequest(BaseModel):
    username: str
    message: str


class ChatRoom(BaseModel):
    name: str
    messages: List[MessageRequest] = []
