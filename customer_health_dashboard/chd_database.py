# database.py creates a database session that can be used in multiple files. 
# It also creates a context variable to manage the session. 
# The get_db() function is a dependency used in other files to get the database session. 
# This is used for managing database connections and sessions in a FastAPI application.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar, copy_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./data_generation/cs_health_dashboard_snake_case.db"
#SQLALCHEMY_DATABASE_URL = "sqlite:///./data_generation/cs_health_dashboard.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Context variable to manage session
session_context: ContextVar[Session] = ContextVar("session_context")

# Copy the current context
context = copy_context()

def get_db():
    db = SessionLocal()
    token = context.run(session_context.set, db)
    try:
        yield db
    finally:
        context.run(session_context.reset, token)
        db.close()