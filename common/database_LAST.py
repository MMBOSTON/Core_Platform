from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextvars import ContextVar

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Replace with your database URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Context variable to manage session
session_context: ContextVar[Session] = ContextVar("session_context")

def get_db():
    db = SessionLocal()
    token = session_context.set(db)
    try:
        yield db
    finally:
        session_context.reset(token)
        db.close()

