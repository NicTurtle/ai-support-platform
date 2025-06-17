from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.db.models.user_session import UserSession
from app.models.user_session import UserSessionCreate


class UserSessionService:
    @staticmethod
    async def create_session(db: AsyncSession, data: UserSessionCreate) -> UserSession:
        session = UserSession(
            id=uuid4(),
            user_id=data.user_id,
            channel=data.channel,
            thread_id=data.thread_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_latest_session_by_user(db: AsyncSession, user_id: UUID) -> UserSession | None:
        result = await db.execute(
            select(UserSession)
            .where(UserSession.user_id == user_id)
            .order_by(UserSession.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_last_seen(db: AsyncSession, session_id: UUID) -> None:
        await db.execute(
            update(UserSession)
            .where(UserSession.id == session_id)
            .values(updated_at=datetime.utcnow())
        )
        await db.commit()
