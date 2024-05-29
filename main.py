# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from common.database import SessionLocal, engine, Base
from user_management import models, routes as user_routers
from common.logging_config import setup_logging
from common.config import DATABASE_URL
from auth.jwt_handler import verify_token  # Importing from jwt_handler
from common.middlewares import setup_middlewares  # Importing the middleware setup function

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = setup_logging()  # Setup logging TODO: Add logging to a timestamped files for each run

# Event handlers for startup and shutdown
@app.on_event("startup")
async def startup_event():
    logger.info("Application started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

    
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

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the FastAPI application"}

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    errors = exc.errors()
    error_messages = []
    for error in errors:
        loc = error.get("loc")
        msg = error.get("msg")
        error_messages.append(f"Error at {loc}: {msg}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )

# Include user routes
app.include_router(user_routers.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    setup_middlewares(app)  # Apply the middleware
    uvicorn.run(app, host="0.0.0.0", port=8000)