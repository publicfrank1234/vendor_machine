from typing import Dict

from fastapi import APIRouter, HTTPException

from app.models import User
from app.schemas import UserCreate, UserDisplay, UserUpdate

router = APIRouter()
users: Dict[int, User] = {}  # This will act as our "database"
user_id_counter: int = 1


@router.post("/users/", response_model=UserDisplay)
def create_user(user: UserCreate):
    global user_id_counter
    if user.username in [u.username for u in users.values()]:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = f"hashed-{user.password}"  # Simulate password hashing
    new_user = User(
        id=user_id_counter,
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
    )
    users[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


@router.get("/users/{user_id}", response_model=UserDisplay)
def get_user(user_id: int):
    if user_id in users:
        return users[user_id]
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{user_id}", response_model=UserDisplay)
def update_user(user_id: int, user_update: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username in [u.username for u in users.values() if u.id != user_id]:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Update user details
    user = users[user_id]
    user.username = user_update.username
    user.hashed_password = f"hashed-{user_update.password}"  # Simulate password hashing
    user.role = user_update.role
    return user


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return {"message": "User deleted successfully"}
