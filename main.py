from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from common.database import SessionLocal, engine, Base
from user_management import models as user_models, routes as user_routers
from customer_health_dashboard import chd_models, chd_routes
from customer_health_dashboard.chd_middlewares import setup_chd_middlewares
from common.logging_config import setup_logging
from auth.jwt_handler import verify_token
from common.middlewares import setup_common_middlewares, test_function
from customer_health_dashboard.chd_models import Customer
from customer_health_dashboard.chd_schemas import CustomerCreate  # Adjust the import path as necessary

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%m/%d/%Y %H:%M:%S',
                handlers=[
                    logging.FileHandler('app.log'),
                    logging.StreamHandler()])

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

test_function()  # This should print the success message if imports work correctly.

# Conditionally apply middleware based on the context
if "customer_health_dashboard" in __file__:
    setup_chd_middlewares(app)
else:
    setup_common_middlewares(app)

# Define a list of allowed origins for CORS
origins = [
    "http://localhost:3000",  # React app URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn")

# Define the function first
async def startup_event():
    print("Application starting")
    logger.info("Application started [message from startup_event() in main.py]")

# Then add the event handler
app.add_event_handler("startup", startup_event)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the startup function
def startup():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection successful [message from startup() in main.py].")
    except SQLAlchemyError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Add the startup event handler
app.add_event_handler("startup", startup)

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    print(f"Request: {request}")
    print(f"Exception: {exc}")
    errors = exc.errors()
    error_messages = ", ".join([f"Error at {error['loc']}: {error['msg']}" for error in errors])
    print(f"Validation errors: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )

# Include user routes
app.include_router(user_routers.router, prefix="/users", tags=["users"])
app.include_router(chd_routes.router, prefix="/dashboard", tags=["dashboard"])

def process_customers_data(customers):
    return [{"customer_id": customer.id, "name": customer.name, "nps_score": customer.nps_score} for customer in customers]

@app.get("/customer/{customer_id}")
async def get_customer_health(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(chd_models.Customer).filter(chd_models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/customers")
async def get_all_customers(db: Session = Depends(get_db)):
    customers_all = db.query(chd_models.Customer).all()
    return customers_all

# Define the shutdown function
async def shutdown_event():
    logger.info("Application shutting down")

# Add the shutdown event handler
app.add_event_handler("shutdown", shutdown_event)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)