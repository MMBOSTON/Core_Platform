
"""TODO: This MAY need to be updated in all the other CRUD functions as well."""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from user_management import schemas, models
from dotenv import load_dotenv
import os
import jwt

load_dotenv()  # Load environment variables from .env.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user in the database was modified to add ".__dict__" to the return statement.
    This is because the response model in the route expects a dictionary. """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=user.password, hashed_password=hashed_password)
    #db_user = models.User(username=user.username, password=user.password)  # commented out to test new ChatGPT code.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.__dict__


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# not included by ChatGPT code - added manually.
def verify_user(db: Session, user: schemas.UserCreate):
    db_user = get_user_by_username(db, user.username)
    if db_user and pwd_context.verify(user.password, db_user.hashed_password):
        return True
    return False

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# not included by ChatGPT code - added manually.
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# not included by ChatGPT code - added manually.
def get_all_users(db: Session):
    return db.query(models.User).all()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = user.username

        if user.password:
            db_user.password = user.password
        # RSL added the following line to check that the hash password is not None
        if user.hashed_password:
            db_user.hashed_password = pwd_context.hash(user.password) # Added this line to hash the password
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
