from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1 import chat
from app.db.init_db import init_db
from app.web.pages import router as pages_router
from app.middleware.cookies import UserIDCookieMiddleware

API_PREFIX = "/api/v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="AI Support Platform Template",
    lifespan=lifespan
)

app.add_middleware(UserIDCookieMiddleware)

app.include_router(pages_router)  # HTML
app.include_router(chat.router, prefix=API_PREFIX, tags=["chat"])
