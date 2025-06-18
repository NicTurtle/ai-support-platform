"""Database initialization utilities."""

from app.db import models
from app.db.session import Base, engine

async def init_db() -> None:
    """Create database tables if they do not exist."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
