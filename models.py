from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class User(BaseModel):
    id: UUID
    names: str
    email: str
    password: str


class Generations(BaseModel):
    gen_id:UUID
    prompt: str
    response: str
    created_at: str


# class UserPrompts(BaseModel):
#     prompt_id: UUID
#     prompt_used: str
