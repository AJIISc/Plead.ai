from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import os

DATABASE_URL = "postgresql://anurajmaurya:anurajmaurya@localhost/plead_staging_db"  # Update with your actual database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database connection
def get_db_conn():
    conn = psycopg2.connect(
        dbname="plead_staging_db",
        user=os.getenv("DB_USER", "anurajmaurya"),
        password=os.getenv("DB_PASSWORD", "anurajmaurya"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn