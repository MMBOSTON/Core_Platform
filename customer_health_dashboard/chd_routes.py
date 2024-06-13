from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from fastapi import HTTPException
from common.schemas import CustomerCreate
from common.models import Customer, Customer_Base  
from customer_health_dashboard.chd_database import get_db
import logging

router = APIRouter()

# Setup logging
logger = logging.getLogger(__name__)

@router.post("/dashboard", response_model=Customer_Base, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = Customer(
            name=customer.name,
            email=customer.email,
            tel_number=customer.tel_number,
            signup_date=customer.signup_date,
            nps_score=customer.nps_score,
            ces_score=customer.ces_score
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        logger.info(f"Customer created with ID: {db_customer.id}")
        return Customer_Base.from_orm(db_customer)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create customer")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/customer", response_model=List[Customer_Base])
async def get_all_customer(db: Session = Depends(get_db)):
    try:
        customers = db.query(Customer).all()
        logger.info("Retrieved all customers")
        return [Customer_Base.from_orm(customer) for customer in customers]
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving customers: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve customers")

@router.get("/customer/{customer_id}", response_model=Customer_Base)
async def get_customer_health(customer_id: int, db: Session = Depends(get_db)):
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            logger.warning(f"Customer with ID {customer_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        logger.info(f"Retrieved customer with ID: {customer_id}")
        return Customer_Base.from_orm(customer)
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving customer with ID {customer_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve customer")

@router.get("/dashboard_data", response_model=List[Customer_Base])
def get_dashboard_data(db: Session = Depends(get_db)):
    try:
        data = db.query(Customer).all()
        logger.info("Retrieved dashboard data")
        return [Customer_Base.from_orm(customer) for customer in data]
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving dashboard data: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve dashboard data")