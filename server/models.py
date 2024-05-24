from pydantic import BaseModel


class MessageRequest(BaseModel):
    username: str
    message: str
