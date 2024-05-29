# routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user_management import user_crud, schemas
from common.database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserCreate)  # Use UserCreate schema as the response model
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_crud.create_user(db=db, user=user)
