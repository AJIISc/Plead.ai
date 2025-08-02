from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from fastapi.middleware.cors import CORSMiddleware
from app.blockchain.create_account import create_account
router = APIRouter()

# Pydantic model for request validation
class SignupRequest(BaseModel):
    name: str
    phone_number: str
    email: str
    password: str
    address: str
    user_type: str  # individual or enterprise
    role: str       # internal employee, user, legal counsel, arbitrator

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="plead_staging_db",
        user=os.getenv("DB_USER", "anurajmaurya"),
        password=os.getenv("DB_PASSWORD", "anurajmaurya"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    return conn

@router.post("/signup")
async def signup(request: SignupRequest):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    public_key, private_key = create_account()
    try:
        cursor.execute(
            """
            INSERT INTO plead_user_information (name, phone_number, email, password, address, user_type, role, public_key, private_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (request.name, request.phone_number, request.email, request.password, request.address, request.user_type, request.role, public_key, private_key)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return {"message": "User signed up successfully"}
