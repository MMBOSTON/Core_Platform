# auth_utils.py
from sqlalchemy.orm import Session
from.models import User  # Adjust the import path according to your project structure
from .password_utils import verify_password

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):  # Ensure you have a verify_password function
        return False
    return user