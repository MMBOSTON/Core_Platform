from sqlalchemy import Column, Integer, String
from customer_health_dashboard.chd_database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=True)  # Raw password (store only if needed)
    hashed_password = Column(String, nullable=False)  # Hashed password (always store)
