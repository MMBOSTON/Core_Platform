# Import the necessary Python Standard Library utility modules
import sys
import os

# Correctly append the directory of main.py to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import time 
import datetime
import requests
import webbrowser
import threading

import uvicorn

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth.jwt_handler import verify_token

from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

# Developer defined modules
from common.logging_config import setup_logging
from customer_health_dashboard.chd_database import SessionLocal, engine, Base, get_db
from user_management import routes as user_routers
from customer_health_dashboard import chd_routes
from customer_health_dashboard.chd_middlewares import setup_chd_middlewares

from common.middlewares import setup_common_middlewares
from common.models import Customer

import logging # REMOVE BASED ON PHIND SUGGESTION TO REMOVE REDUNDANT LOGGING CONFIGURATION ??


logger = logging.getLogger("app")

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# create a instance of the FastAPI class
app = FastAPI()

#test_function()  # This should print the success message if imports work correctly.

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

# Define the function first
async def startup_event():
    #logger = logging.getLogger("app")      # Redundant logging configuration
    logger.info("Application starting")
    logger.info("Application started [message from startup_event() in main.py]")

# Then add the event handler
app.add_event_handler("startup", startup_event)

# Define the startup function
def startup():
    try:
        db = next(get_db())  # Use the get_db function from database.py
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
    logger.error(f"Validation exception: {exc}")
    errors = exc.errors()
    error_messages = ", ".join([f"Error at {error['loc']}: {error['msg']}" for error in errors])
    logger.error(f"Validation errors: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )

# Include user routes
app.include_router(user_routers.router, prefix="/users", tags=["users"])
app.include_router(chd_routes.router, prefix="/dashboard", tags=["dashboard"])

def process_customers_data(customers):
    logger.info("Processing customer data")
    result = [{"customer_id": customer.id, "name": customer.name, "nps_score": customer.nps_score} for customer in customers]
    logger.info("Processed customer data")
    return result 


@app.get("/customer/{customer_id}")
async def get_customer_health(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching customer with ID: {customer_id}")
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        logger.warning(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    logger.info(f"Fetched customer: {customer}")
    return customer

@app.get("/customers")
async def get_all_customers(db: Session = Depends(get_db)):
    logger.info("Fetching all customers")
    customers_all = db.query(Customer).all()
    logger.info(f"Fetched {len(customers_all)} customers")    
    return customers_all

# Define the shutdown function
async def shutdown_event():
    logger.info("Application shutting down")

# Add the shutdown event handler
app.add_event_handler("shutdown", shutdown_event)

def open_browser():
    """
    Start client side of the application in the browser.
    Delays for 2 seconds to ensure the server has started.
    """
    time.sleep(2.5)  # Delay to ensure the server has started
    webbrowser.open("http://127.0.0.1:8000/docs")
    logger.info("Browser opened")

# Your FastAPI application code goes here

if __name__ == "__main__":
    # create logger 
    # logger = logging.getLogger(__name__)
    logger = setup_logging()
    logger.info("Server is starting")
    threading.Thread(target=open_browser).start()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug", reload=True)