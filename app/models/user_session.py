from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal


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
