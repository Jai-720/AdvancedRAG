from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    answer: str

class UserCreate(BaseModel):
    username:str
    password:str