# app/database.py
# Database configuration with environment variable support
# ==========================================================

from dotenv import load_dotenv
load_dotenv()  # Load .env variables from the project root

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import logging

# ----------------------------------------------------------
# Setup basic logging
# ----------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ----------------------------------------------------------
# Build DATABASE_URL dynamically (from .env or fallback vars)
# ----------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB = os.getenv("MYSQL_DB")

    if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB]):
        raise RuntimeError(
            "❌ Missing database credentials! Please set MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DB in your .env file."
        )

    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

logging.info(f"📦 Connecting to database: {DATABASE_URL}")

# ----------------------------------------------------------
# SQLAlchemy Engine and Session Factory
# ----------------------------------------------------------
try:
    engine = create_engine(
        DATABASE_URL,
        echo=True,            # Show SQL logs (turn off in production)
        pool_pre_ping=True,   # Ensures connection is valid
        future=True
    )
except Exception as e:
    logging.error(f"❌ Failed to create SQLAlchemy engine: {e}")
    raise

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ----------------------------------------------------------
# Dependency for FastAPI routes
# ----------------------------------------------------------
def get_db():
    """
    Dependency for FastAPI routes — opens a DB session
    and ensures it's closed after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
