from fastapi import APIRouter, HTTPException, Depends, Response, Cookie, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db_connection, get_db_conn
from app.db.models import User  # Adjust based on your actual model imports
import jwt
from datetime import datetime, timedelta
import logging
from psycopg2.extras import RealDictCursor
from app.api.v1.utils import SECRET_KEY, ALGORITHM
router = APIRouter()

logger = logging.getLogger(__name__)



def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    token = jwt.encode({"sub": user_id, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
    return token

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None, db: Session = Depends(get_db_connection)):
    print(f"Form data: {form_data.username}")
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.verify_password(form_data.password):  # Assuming you have a method to verify password
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create JWT token
    print(f"User: {user}")
    token = create_jwt_token(user.id)
    logger.info(f"Token: {token}")
    # Set the token in an HTTP-only cookie
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True)  # Set secure=True for HTTPS

    # Optionally, create an entry in the database if needed
    conn = get_db_conn()  # Get the connection direct
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Verify user credentials
        cursor.execute(
            """
            SELECT id, user_type, role FROM plead_user_information
            WHERE email = %s AND password = %s
            """,
            (user.email, user.password)
        )

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Record login information
        cursor.execute(
            """
            INSERT INTO plead_user_login (user_id, user_type, role, login_time)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id
            """,
            (user.id, user.user_type, user.role)
        )
        login_id = cursor.fetchone()['id']
        conn.commit()
        token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm=ALGORITHM)

        return {"message": "Login successful", "login_id": login_id, "token": token}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()  # Close the connection manually

    return {"message": "Login successful"}

def get_current_user(authorization: str = Header(None)):
    print(f"Authorization: {authorization}")
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Extract the token from the "Bearer <token>" format
    token = authorization.split(" ")[1] if " " in authorization else None

    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        print(f"User ID: {user_id}")
        return user_id  # You can also return the user object if needed
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/test")
async def test_endpoint():
    return {"message": "Test endpoint is working!"}