from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserResponse

# Змінили назву на user_router, щоб уникнути конфліктів імен
user_router = APIRouter()

# 🧠 Емуляція бази даних через звичайний словник
FAKE_USERS_DB = {
    1: {"id": 1, "email": "denys@example.com", "username": "shvaikovskyi", "full_name": "Denys Shvaikovskyi", "is_active": True},
    2: {"id": 2, "email": "test@example.com", "username": "tester", "full_name": "John Doe", "is_active": True}
}

id_counter = 3

# 1. GET ALL
@user_router.get("/", response_model=List[UserResponse])
def get_users():
    return list(FAKE_USERS_DB.values())

# 2. GET BY ID
@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in FAKE_USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")
    return FAKE_USERS_DB[user_id]

# 3. POST
@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate):
    global id_counter
    for user in FAKE_USERS_DB.values():
        if user["email"] == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    new_user_data = user_in.model_dump()
    new_user_data["id"] = id_counter
    new_user_data["is_active"] = True
    new_user_data.pop("password", None)
    
    FAKE_USERS_DB[id_counter] = new_user_data
    id_counter += 1
    return new_user_data

# 4. PUT
@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate):
    if user_id not in FAKE_USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")
        
    current_user_data = FAKE_USERS_DB[user_id]
    update_data = user_in.model_dump(exclude_unset=True)
    
    for field in update_data:
        if field != "password":
            current_user_data[field] = update_data[field]
            
    FAKE_USERS_DB[user_id] = current_user_data
    return current_user_data

# 5. DELETE
@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in FAKE_USERS_DB:
        raise HTTPException(status_code=404, detail="User not found")
    
    del FAKE_USERS_DB[user_id]
    return None