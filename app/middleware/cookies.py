from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from uuid import uuid4

class UserIDCookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        user_id = request.cookies.get("user_id")
        response: Response = await call_next(request)

        if not user_id:
            user_id = str(uuid4())
            response.set_cookie("user_id", user_id, max_age=60*60*24*30, httponly=True)

        return response