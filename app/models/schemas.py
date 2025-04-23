from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    user_email: str

class ChatResponse(BaseModel):
    reply: str
    ticket_created: bool = False
