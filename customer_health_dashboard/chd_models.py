from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from common.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    tel_number = Column(String)
    signup_date = Column(Date)
    nps_score = Column(Integer)
    ces_score = Column(Integer)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    issue_date = Column(Date)
    status = Column(String)
    severity = Column(String)

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    interaction_date = Column(Date)
    satisfaction_score = Column(Integer)

class CustomerHealthScore(Base):
    __tablename__ = "customer_health_scores"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    health_score = Column(Integer)

class RenewalDates(Base):
    __tablename__ = "renewal_dates"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    renewal_date = Column(Date)

class BillingInformation(Base):
    __tablename__ = "billing_information"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    billing_status = Column(String)

class OnboardingStatus(Base):
    __tablename__ = "onboarding_statuses"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    onboarding_status = Column(String)

class UpsellOpportunities(Base):
    __tablename__ = "upsell_opportunities"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    opportunity = Column(String)

class ProductUsage(Base):
    __tablename__ = "product_usage"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    usage_duration = Column(Integer)
    features_used = Column(Integer)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    feedback_text = Column(String)
    feedback_date = Column(Date)

class ChurnRisk(Base):
    __tablename__ = "churn_risk"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    churn_risk_score = Column(Integer)
    churn_risk_reasons = Column(String)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    contact_name = Column(String)
    contact_role = Column(String)
    contact_email = Column(String)
