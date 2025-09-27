# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Base
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ----------------------
# Database URL
# ----------------------
# Example for SQLite (MVP)
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./webhook_router.db")

# Example for Postgres (optional later)
# DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/webhook_router")

# ----------------------
# Engine & Session
# ----------------------
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {},
    echo=True  # Set to True for SQL debugging
)

# Scoped session for thread-safe access in FastAPI
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# ----------------------
# Create Tables
# ----------------------
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
