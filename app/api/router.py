from fastapi import APIRouter
from app.api.endpoints import users

api_router = APIRouter()

# Тепер ми чітко викликаємо users.user_router, і Python його 100% побачить!
api_router.include_router(users.user_router, prefix="/users", tags=["users"])