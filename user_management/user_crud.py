from sqlalchemy.orm import Session
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from common.models import User  # Assuming `User` is your SQLAlchemy model
from common.schemas import UserResponse  # Adjust the import path as necessary

from common.schemas import UserBase, UserCreate, UserUpdate
from common import models
from dotenv import load_dotenv
from .password_utils import hash_password, verify_password
from auth.jwt_handler import verify_token  # Importing from jwt_handler
import os
import jwt
import logging

load_dotenv()  # Load environment variables from .env.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        logger.info(f"User {username} not found")
        return None
    if not verify_password(password, user.hashed_password):
        logger.info(f"Password match for user {username}: False")
        return None
    logger.info(f"Password match for user {username}: True")
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):  # Ensure you have a verify_password function
        return False
    return user

def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = hash_password(user.password)
        db_user = models.User(username=user.username, password=user.password, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return None

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    return None


def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> list[dict]:
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.from_orm(user).dict() for user in users]


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        if user.password:
            db_user.hashed_password = pwd_context.hash(user.password)
        db.commit()
        db.refresh(db_user)
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    return None

def get_users_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).all()

def get_users_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).all()

def update_user_by_username(db: Session, username: str, user: UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        db_user.username = user.username
        if user.password:
            db_user.hashed_password = pwd_context.hash(user.password)
        db.commit()
        db.refresh(db_user)
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    return None

def delete_user_by_username(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    return None