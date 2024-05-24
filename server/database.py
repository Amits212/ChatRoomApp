from typing import List
from models import MessageRequest

messages: List[MessageRequest] = []

def get_messages() -> List[MessageRequest]:
    return messages

def add_message(message: MessageRequest):
    messages.append(message)