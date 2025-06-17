from pydantic import BaseModel, EmailStr
from typing import Annotated


class UserCreate(BaseModel):
    email: Annotated[EmailStr, ...]
    password: Annotated[str, ...]


class UserLogin(BaseModel):
    email: Annotated[EmailStr, ...]
    password: Annotated[str, ...]


class UserPublic(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # Чтобы работать с ORM


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
