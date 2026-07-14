from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    names: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    names: str
    email: str
    created_at: datetime

class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000)

class GenerationResponse(BaseModel):
    id: int
    user_id: int
    prompt: str
    response: str
    created_at: datetime
    cached: bool = False