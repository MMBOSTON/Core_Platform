# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar, copy_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Ensure this path is correct

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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