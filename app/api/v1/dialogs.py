from fastapi import APIRouter
from app.models.dialog import MessageInput, MessageOutput

router = APIRouter(prefix="/dialogs", tags=["Dialogs"])

@router.get("/ping")
async def ping():
    return {"status": "ok"}

@router.post("/message", response_model=MessageOutput)
async def send_message(msg: MessageInput):
    # Заглушка: пока возвращаем просто эхо
    return {"response": f"You said: {msg.message}"}
