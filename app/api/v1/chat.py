from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.models.user_session import UserSessionCreate
from app.services.user_session import UserSessionService
from app.external.openai import ask_gpt_with_memory, create_thread

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@router.post("/chat")
async def chat_with_bot(
    body: ChatRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_session),
):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id in cookie")

    user_uuid = UUID(user_id)
    latest_session = await UserSessionService.get_latest_session_by_user(db, user_uuid)

    if latest_session and latest_session.thread_id:
        thread_id = latest_session.thread_id
        await UserSessionService.update_last_seen(db, latest_session.id)
    else:
        thread_id = await create_thread()
        await UserSessionService.create_session(
            db,
            data=UserSessionCreate(
                user_id=user_uuid,
                channel="web",
                thread_id=thread_id,
            )
        )

    response = await ask_gpt_with_memory(
        message=body.message,
        thread_id=thread_id,
    )

    return {"response": response}
