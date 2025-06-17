from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from uuid import uuid4

from app.db.session import async_session
from app.models.user_session import UserSessionCreate
from app.services.user_session import UserSessionService

class UserIDCookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_id = request.cookies.get("user_id")

        if not user_id:
            user_uuid = uuid4()
            async with async_session() as session:
                await UserSessionService.create_session(
                    session,
                    UserSessionCreate(user_id=user_uuid, channel="web", thread_id=None),
                )
            response: Response = await call_next(request)
            response.set_cookie(
                "user_id",
                str(user_uuid),
                max_age=60 * 60 * 24 * 30,
                httponly=True,
            )
            return response

        response: Response = await call_next(request)
        return response
