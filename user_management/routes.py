from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user_management import schemas, user_crud
from common.database import get_db
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Received login attempt for username: {user.username}")
    db_user = user_crud.verify_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = user_crud.create_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


# @router.post("/login", response_model=schemas.UserResponse)
# def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     if not user_crud.verify_user(db, user):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     db_user = user_crud.get_user_by_username(db, username=user.username)
#     return db_user

@router.get("/users", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = user_crud.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.update_user(db, user_id, user)

@router.delete("/{user_id}", response_model=None)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user(db, user_id)
    return {"detail": "User successfully deleted"}