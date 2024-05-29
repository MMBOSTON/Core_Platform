from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from user_management import user_crud, schemas
from common.database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return schemas.UserResponse.from_orm(user_crud.create_user(db=db, user=user))

@router.get("/users", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return [schemas.UserResponse.from_orm(user) for user in users]

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.from_orm(db_user)

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse.from_orm(db_user)

# @router.delete("/users/{user_id}", response_model=schemas.UserResponse)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.delete_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return schemas.UserResponse.from_orm(db_user)

# @router.delete("/users/{user_id}", response_model=schemas.UserResponse)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.delete_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     elif db_user is not None:
#         return schemas.UserResponse.from_orm(db_user)
#     else:
#         raise HTTPException(status_code=500, detail="Unexpected error occurred")

@router.delete("/{user_id}", response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif isinstance(db_user, str):
        raise HTTPException(status_code=400, detail=db_user)
    else:
        return schemas.UserResponse.from_orm(db_user)


