from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db_connection
from app.db.models import plead_user_connections, plead_offers, User  # Adjust based on your actual model imports
from app.api.v1.auth.auth import get_current_user  # Import your authentication logic
from app.api.v1.auth.utility import get_public_key
import logging
import uuid
import json

logger = logging.getLogger(__name__)

router = APIRouter()

class OfferRequest(BaseModel):
    contract_title: str
    contract_details: dict
    user_id: int  # The ID of the user to whom the offer is sent
    contract_type: str

@router.post("/send-offer")
async def send_offer(
    request: OfferRequest,
    db: Session = Depends(get_db_connection),
    current_user: str = Depends(get_current_user)  # Automatically gets the current user from the JWT token
):
    print(f"Sending offer from user ID: {current_user} to user ID: {request.user_id}")

    # Check if the recipient user exists
    recipient_connection = db.query(plead_user_connections).filter(
        plead_user_connections.connection_id == request.user_id,
        plead_user_connections.user_id == current_user
    ).first()

    if not recipient_connection:
        raise HTTPException(status_code=404, detail="Recipient user not found in your connections.")
    print(f"Request: {request}")    
    # Create a new offer
    # contract_details = json.loads(request.contract_details
    if request.contract_type == "CUSTOM CONTRACT":
        contract_details = request.contract_details['details']
    else:
        contract_details = str(request.contract_details)
    new_offer = plead_offers(
        contract_id=None,  # Assuming you have a contract_id to link, set it accordingly
        sender_id=current_user,
        receiver_id=request.user_id,
        offer_details=contract_details,
        contract_title=request.contract_title,
        offer_status='pending',
        contract_type=request.contract_type,
        sender_public_key=get_public_key(current_user),
        receiver_public_key=get_public_key(request.user_id)
    )

    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)

    return {"message": "Offer sent successfully!", "offer_id": new_offer.offer_id}

@router.get("/pending-offers")
async def get_pending_offers(
    db: Session = Depends(get_db_connection),
    current_user: str = Depends(get_current_user)
):
    print(f"Current user: {current_user}")
    pending_offers = []
    for offer in db.query(plead_offers).filter(
        plead_offers.receiver_id == current_user ,
        plead_offers.offer_status == 'pending'
    ).all():
        pending_offers.append({
            "offer_id": offer.offer_id,
            "contract_id": offer.contract_id,
            "sender_id": offer.sender_id,
            "sender_name": db.query(User).filter(User.id == offer.sender_id).first().name,
            "receiver_id": offer.receiver_id,
            "offer_details": offer.offer_details,
            "offer_status": offer.offer_status,
            "contract_type": offer.contract_type,
            "sender_public_key": offer.sender_public_key,
            "receiver_public_key": offer.receiver_public_key,
            "contract_title": offer.contract_title
        })
    print(f"Pending offers: {pending_offers}")
    return {"pending_offers": pending_offers}   