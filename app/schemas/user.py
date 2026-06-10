from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Базові поля, які є у юзера взагалі
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

# Схема для створення юзера (тут обов'язковий пароль)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

# Схема для оновлення юзера (всі поля необов'язкові, міняємо що хочемо)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)

# Схема, яку сервер віддає клієнту у відповідь (Response)
class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True