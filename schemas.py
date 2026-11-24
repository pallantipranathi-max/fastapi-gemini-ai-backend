from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class PromptRequest(BaseModel):
    prompt: str
