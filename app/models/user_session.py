"""Pydantic models for user session data transfer objects."""

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel


class UserSessionCreate(BaseModel):
    user_id: UUID
    channel: Literal["web"]
    thread_id: Optional[str] = None


class UserSessionRead(UserSessionCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    assistant_id: Optional[str] = None

    class Config:
        from_attributes = True
