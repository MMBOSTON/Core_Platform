from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=100)

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode: True

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str
    password: str


