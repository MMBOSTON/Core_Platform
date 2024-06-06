from pydantic import BaseModel, Field, validator
from typing import Optional
from .password_utils import hash_password, verify_password

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

    @validator('password', pre=True)
    def hash_user_password(cls, password: str):
        return hash_password(password)

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6, max_length=100)

    @validator('password', pre=True)
    def hash_user_password(cls, password: str):
        if password:
            return hash_password(password)

class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        from_attributes = True

class UserResponse(User):
    pass

class UserLogin(BaseModel):
    username: str
    password: str

class ValidationError(BaseModel):
    loc: str
    msg: str
    type: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    id: int
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str