from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from models import MessageRequest, ChatRoom

client = AsyncIOMotorClient('mongodb://mongo:27017')
db = client.db
rooms_collection = db.rooms


async def get_messages(room_name: str) -> List[MessageRequest]:
    room = await rooms_collection.find_one({"name": room_name})
    if room:
        return room['messages']
    else:
        return []


async def add_message(room_name: str, message: MessageRequest):
    await rooms_collection.update_one({"name": room_name}, {"$push": {"messages": message.dict()}}, upsert=True)


async def add_room(room: ChatRoom):
    await rooms_collection.insert_one(room.dict())


async def get_rooms():
    cursor = rooms_collection.find({})
    rooms = await cursor.to_list(length=100)
    return [ChatRoom(**room) for room in rooms]
