from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db_connection
from app.db.models import User, plead_user_connections  # Adjust based on your actual model imports
from app.api.v1.auth.auth import get_current_user  # Import your authentication logic
import logging
import uuid
from app.api.v1.auth.utility import get_public_key

logger = logging.getLogger(__name__)

router = APIRouter()

class ConnectionRequest(BaseModel):
    identifier: str  # This can be an email or phone number

@router.post("/connections")
async def add_connection(
    request: ConnectionRequest,
    db: Session = Depends(get_db_connection),
    current_user: str = Depends(get_current_user)  # Automatically gets the current user from the JWT token
):
    logger.info(f"Request: {request}")
    
    # Check if the user exists based on the identifier (email or phone number)
    user = db.query(User).filter(
        (User.email == request.identifier) | (User.phone_number == request.identifier)
    ).first()
    
    logger.info(f"User found: {user}")
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = current_user  # Ensure user_id is a UUID
    friend_id = user.id  
    logger.info(f"Current User ID: {user_id}, Friend ID: {friend_id}")
    
    # Add to plead_user_connections
    connection = plead_user_connections(user_id=user_id, connection_id=friend_id, user_public_key=user.public_key, connection_public_key=get_public_key(friend_id))
    db.add(connection)
    db.commit()
    db.refresh(connection)

    return {"message": "Connection created successfully"}

@router.get("/connections")
async def get_connections(
    db: Session = Depends(get_db_connection),
    current_user: str = Depends(get_current_user)  # Automatically gets the current user from the JWT token
):
    logger.info(f"Fetching connections for user ID: {current_user}")

    # Fetch connection IDs for the current user
    connections = db.query(plead_user_connections).filter(plead_user_connections.user_id == current_user).all()
    
    if not connections:
        return {"message": "No connections found."}

    # Fetch user details for each connection
    connection_details = []
    for connection in connections:
        friend_user = db.query(User).filter(User.id == connection.connection_id).first()
        if friend_user:
            connection_details.append({
                "connection_id": connection.connection_id,
                "friend_name": friend_user.name,  # Assuming User model has a 'name' field
                "friend_email": friend_user.email,  # Assuming User model has an 'email' field
                "friend_phone": friend_user.phone_number  # Assuming User model has a 'phone_number' field
            })

    return {"connections": connection_details}
