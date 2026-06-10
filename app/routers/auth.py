from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.models import User
from app.schemas.auth import UserRegister, UserLogin, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
   
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Цей email вже зареєстрований")
        
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password), 
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user_data: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неправильний email або пароль")
        
    
    access_token = create_access_token(data={"sub": user.email})
    
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,   
        max_age=3600,    
        samesite="lax",
        secure=False     
    )
    return {"message": "Вхід успішний"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Ви вийшли з системи"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/my-orders")
async def get_my_orders(current_user: User = Depends(get_current_user)):
    return {
        "user": current_user.name,
        "info": "Доступ дозволено!",
        "mock_orders": [
            {"id": 101, "item": "Laptop", "status": "In delivery"},
            {"id": 102, "item": "Keyboard", "status": "Paid"}
        ]
    }