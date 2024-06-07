from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from user_management import user_crud
from customer_health_dashboard.chd_database import Base, get_db, SessionLocal, engine
#from common.database import get_db, SessionLocal, engine  # remove me !! 
from auth.jwt_handler import create_access_token
from user_management.user_crud import authenticate_user  # Adjust the import path according to your project structure
from common.schemas import User, UserBase, UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenResponse
from typing import Dict

from datetime import timedelta
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user


@router.post("/login", response_model=UserResponse)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Received login attempt for username: {user_login.username}")
    user = user_crud.get_user_by_username(db, user_login.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    password_valid = user_crud.verify_password(user_login.password, user.hashed_password)
    logger.info(f"Password match: {password_valid}")

    if not password_valid:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = user_crud.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.update_user(db, user_id, user)

# @router.delete("/{user_id}", response_model=None)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     user_crud.delete_user(db, user_id)
#     return {"detail": "User successfully deleted"}

@router.delete("/{user_id}", response_model=Dict[str, str])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user(db, user_id)
    return {"detail": "User successfully deleted"}
