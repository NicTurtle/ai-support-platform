"""Utility functions for interacting with the OpenAI Assistants API."""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from openai import AsyncOpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from app.config import settings

# Configure the OpenAI async client once and reuse it
client = AsyncOpenAI(api_key=settings.openai_api_key)

logger = logging.getLogger(__name__)

ASSISTANT_ID: str = settings.openai_assistant_id

# Poll interval while waiting for assistant run completion
_POLL_INTERVAL: float = 0.25
_MAX_POLLS: int = 120  # 30 seconds


async def create_thread() -> str:
    """Create a new assistant thread and return its ID."""

    thread: Thread = await client.beta.threads.create()
    return thread.id


async def _wait_for_run_completion(run: Run, thread_id: str) -> Run:
    """Poll the run status until completion or timeout."""

    for _ in range(_MAX_POLLS):
        run_status: Run = await client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        if run_status.status == "completed":
            return run_status
        if run_status.status == "failed":
            raise RuntimeError("Assistant run failed")
        await asyncio.sleep(_POLL_INTERVAL)

    raise TimeoutError("Assistant run timed out")


async def ask_gpt_with_memory(message: str, thread_id: str) -> str:
    """Send a message to the assistant and return the response."""

    try:
        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        run: Run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
        )

        await _wait_for_run_completion(run, thread_id)

        messages = await client.beta.threads.messages.list(
            thread_id=thread_id,
            limit=1,
        )
        for msg in messages.data:
            if msg.role == "assistant" and msg.content:
                response = msg.content[0].text.value
                logger.debug("Assistant response: %s", response)
                return response

        return "[No response from assistant]"
    except Exception as exc:
        logger.exception("OpenAI assistant request failed: %s", exc)
        raise
