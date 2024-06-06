# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi.middleware.cors import CORSMiddleware
from common.database import SessionLocal, engine, Base
from user_management import models, routes as user_routers
from common.logging_config import setup_logging
from common.config import DATABASE_URL
from auth.jwt_handler import verify_token  # Importing from jwt_handler
from common.middlewares import setup_middlewares  # Importing the middleware setup function
from customer_health_dashboard.chd_middlewares import setup_chd_middlewares as setup_chd_middlewares
from customer_health_dashboard import chd_routes  # Import the customer health dashboard routes
from user_management.password_utils import hash_password
import logging
import pandas as pd

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# Define a list of allowed origins for CORS
# In this case, we're allowing requests from our frontend running on localhost:3000
allowed_origins = [
    "http://localhost:3000",
]

# Add CORS middleware
if allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

setup_middlewares(app)
setup_chd_middlewares(app)

logger = logging.getLogger("uvicorn")

# Event handlers for startup and shutdown
@app.on_event("startup")
async def startup_event():
    print("Application starting")
    logger.info("Application started")

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

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    print(f"Request: {request}")
    print(f"Exception: {exc}")
    errors = exc.errors()
    error_messages = []
    for error in errors:
        loc = error.get("loc")
        msg = error.get("msg")
        error_messages.append(f"Error at {loc}: {msg}")
    print(f"Validation errors: {error_messages}")  # Print detailed validation errors
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )


# Include user routes
app.include_router(user_routers.router, prefix="/users", tags=["users"])
app.include_router(chd_routes.router, prefix="/dashboard", tags=["dashboard"])

# Load customer health data
df = pd.read_csv('customer_health_data.csv')

@app.get("/customer/{customer_id}")
async def get_customer_health(customer_id: int):
    customer = df[df['customer_id'] == customer_id]
    if customer.empty:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer.to_dict(orient='records')[0]

@app.get("/customers")
async def get_all_customers():
    return df.to_dict(orient='records')

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

if __name__ == "__main__":
    import uvicorn
    #setup_middlewares(app)  # Apply the middleware
    #setup_chd_middlewares(app)  # Apply the dashboard middleware
    uvicorn.run(app, host="0.0.0.0", port=8000)
