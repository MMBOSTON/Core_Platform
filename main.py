# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from common.database import SessionLocal, engine, Base
from user_management import models, routes as user_routers
from common.logging_config import setup_logging
from common.config import DATABASE_URL
from user_management.user_crud import verify_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = setup_logging()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    # Test database connection
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}

# JWT Middleware
@app.middleware("http")
async def verify_jwt_middleware(request: Request, call_next):
    if request.url.path not in ["/login", "/register"]:
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
            payload = verify_token(token)
            if payload is None:
                logger.info(f"Invalid token: {token}")
                raise HTTPException(status_code=403, detail="Invalid token")
    response = await call_next(request)
    return response

# Include user routes
app.include_router(user_routers.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
