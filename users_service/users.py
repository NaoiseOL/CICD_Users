from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .database import engine, SessionLocal
from .models import Base, UserDB
from .schemas import UserCreate, UserRead, UserUpdate
from .rabbit import publish_event
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    stmt = select(UserDB).order_by(UserDB.user_id)
    result = db.execute(stmt)
    return result.scalars().all()


@app.get("/api/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def add_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = UserDB(**payload.model_dump())
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")

    asyncio.create_task(
        publish_event(
            "user.created",
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "surname": user.surname
            }
        )
    )

    return user


@app.put("/api/users/{user_id}", response_model=UserRead)
async def replace_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = payload.first_name
    user.surname = payload.surname
    user.email = payload.email
    user.age = payload.age
    user.phoneNo = payload.phoneNo
    
    try:
        db.commit()
        db.refresh(user) 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User update failed")

    asyncio.create_task(
        publish_event(
            "user.updated",
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "surname": user.surname
            }
        )
    )
    return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    user = db.get(UserDB, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    asyncio.create_task(
        publish_event(
            "user.deleted",
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "surname": user.surname
            }
        )
    )
    
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/api/users/{user_id}", response_model=UserRead)
async def patch_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User Patch Failed")

    asyncio.create_task(
        publish_event(
            "user.patched",
            {
                "id": user.user_id,
                "first_name": user.first_name,
                "surname": user.surname
            }
        )
    )
    return user