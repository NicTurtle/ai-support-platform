import asyncio
import logging
from typing import Optional

import openai
from openai import AsyncOpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from app.config import settings

# Настраиваем клиента
client = AsyncOpenAI(api_key=settings.openai_api_key)

logger = logging.getLogger(__name__)

ASSISTANT_ID: str = settings.openai_assistant_id


async def create_thread() -> str:
    """Создаёт новый thread и возвращает его ID"""
    thread: Thread = await client.beta.threads.create()
    return thread.id


async def ask_gpt_with_memory(message: str, thread_id: str) -> str:
    """Отправляет сообщение в thread, запускает run и возвращает ответ от ассистента"""
    try:
        # 1. Добавляем сообщение от пользователя
        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

    # 2. Запускаем run ассистента
        run: Run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
        )

    # 3. Ожидаем завершения run
        for _ in range(60):  # максимум 30 секунд
            run_status: Run = await client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise RuntimeError("Assistant run failed")
            await asyncio.sleep(0.5)
        else:
            raise TimeoutError("Assistant run timed out")

        # 4. Получаем последнее сообщение от ассистента
        messages = await client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:  # API returns latest first
            if msg.role == "assistant" and msg.content:
                response = msg.content[0].text.value
                logger.debug("Assistant response: %s", response)
                return response

        return "[No response from assistant]"
    except Exception as e:
        logger.exception("OpenAI assistant request failed: %s", e)
        raise