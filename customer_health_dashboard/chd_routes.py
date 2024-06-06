from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from customer_health_dashboard.chd_models import Customer
#Product, SupportTicket, Interaction, CustomerHealthScore, 
#RenewalDates, BillingInformation, OnboardingStatus, UpsellOpportunities, 
#ProductUsage, Feedback, ChurnRisk, Contact#from common.database import get_db
from customer_health_dashboard.chd_schemas import CustomerCreate, CustomerHealthScore
from customer_health_dashboard.chd_database import get_db

router = APIRouter()

@router.post("/dashboard", response_model=CustomerCreate)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
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
    return db_customer

@router.get("/customer")
async def get_all_customer(db: Session = Depends(get_db)):
    customer = db.query(Customer).all()
    return customer

@router.get("/customer/{customer_id}")
async def get_customer_health(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/dashboard_data")
def get_dashboard_data(db: Session = Depends(get_db)):
    data = db.query(Customer).all()
    return data

