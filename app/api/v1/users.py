# /api/v1/users.py
from uuid import uuid4
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.db.models.user import User
from datetime import datetime

router = APIRouter()

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/guest")
async def create_guest_user(db: AsyncSession = Depends(get_async_session)):
    guest = User(
        id=uuid4(),
        name="Guest",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(guest)
    await db.commit()
    await db.refresh(guest)
    return {"user_id": guest.id}
