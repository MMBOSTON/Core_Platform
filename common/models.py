from pydantic import BaseModel
from datetime import date
from typing import Optional
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from customer_health_dashboard.chd_database import Base, get_db, SessionLocal, engine

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)  # Raw password (store only if needed)
    hashed_password = Column(String, nullable=False)  # Hashed password (always store)

class Customer_Base(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    tel_number: Optional[str] = None
    signup_date: date
    nps_score: int
    ces_score: int

class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    tel_number = Column(String)
    signup_date = Column(Date)
    nps_score = Column(Integer)
    ces_score = Column(Integer)

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Support_Ticket(Base):
    __tablename__ = "support_ticket"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    issue_date = Column(Date)
    status = Column(String)
    severity = Column(String)

class Interaction(Base):
    __tablename__ = "interaction"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    interaction_date = Column(Date)
    satisfaction_score = Column(Integer)

class Customer_Health_Score(Base):
    __tablename__ = "customer_health_score"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    health_score = Column(Integer)

class Renewal_Dates(Base):
    __tablename__ = "renewal_dates"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    renewal_date = Column(Date)

class Billing_Information(Base):
    __tablename__ = "billing_information"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    billing_status = Column(String)

class Onboarding_Status(Base):
    __tablename__ = "onboarding_status"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    onboarding_status = Column(String)

class Upsell_Opportunities(Base):
    __tablename__ = "upsell_opportunities"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    opportunity = Column(String)

class Product_Usage(Base):
    __tablename__ = "product_usage"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    usage_duration = Column(Integer)
    features_used = Column(Integer)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    feedback_text = Column(String)
    feedback_date = Column(Date)

class Churn_Risk(Base):
    __tablename__ = "churn_risk"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    churn_risk_score = Column(Integer)
    churn_risk_reasons = Column(String)

class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    contact_name = Column(String)
    contact_role = Column(String)
    contact_email = Column(String)