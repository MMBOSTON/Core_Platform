from sqlalchemy.orm import Session
from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from user_management import schemas, models
from dotenv import load_dotenv
from .password_utils import hash_password
from auth.jwt_handler import verify_token  # Importing from jwt_handler
import os
import jwt

load_dotenv()  # Load environment variables from .env.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, password=user.password, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
    return user_dict

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_user(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_username(db, username=user.username)
    if db_user and db_user.hashed_password:
        try:
            return verify_password(user.password, db_user.hashed_password)
        except UnknownHashError:
            print("Unknown hash error from verify_user function.")
            return False
    return False

def get_user_by_id(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        user_dict = {key: value for key, value in db_user.__dict__.items() if not key.startswith('_')}
        return user_dict
    return None

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
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

def update_user_by_username(db: Session, username: str, user: schemas.UserUpdate):
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