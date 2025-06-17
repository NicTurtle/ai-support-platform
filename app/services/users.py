from itertools import count
from app.models.user import UserCreate, UserPublic

_id = count(1)

async def create_user(payload: UserCreate) -> UserPublic:
    new_id = next(_id)
    return UserPublic(id=new_id, email=payload.email)
