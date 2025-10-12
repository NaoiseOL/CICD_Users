from fastapi import APIRouter, HTTPException, status
from .schemas import User

router = APIRouter()
users: list[User] = []

@router.get("/")
def get_users():
    return users

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, new_user: User):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users[i] = new_user
            return new_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )