from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from models import MessageRequest

client = AsyncIOMotorClient('mongodb://mongo:27017')
db = client.db
messages_collection = db.messages


async def get_messages() -> List[MessageRequest]:
    cursor = messages_collection.find({})
    messages = await cursor.to_list(length=100)
    return [MessageRequest(**msg) for msg in messages]


async def add_message(message: MessageRequest):
    await messages_collection.insert_one(message.model_dump())
