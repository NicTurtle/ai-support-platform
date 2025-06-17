from fastapi import APIRouter, status
from app.models.user import UserCreate, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    # Заглушка: в реальности — создать пользователя в БД
    return {"access_token": "mock_token", "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    # Заглушка: в реальности — проверка пользователя, генерация токена
    return {"access_token": "mock_token", "token_type": "bearer"}

#Роуты:
#POST /auth/register — регистрация администратора
#POST /auth/login — вход
#GET /auth/me — информация о текущем пользователе
#(дальше будут refresh, logout, change-password)