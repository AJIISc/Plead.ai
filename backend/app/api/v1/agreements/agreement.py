from fastapi import  HTTPException, Depends, APIRouter
from pydantic import BaseModel
from enum import Enum
from app.db.database import get_db_connection
from app.api.v1.auth.auth import get_current_user
from sqlalchemy.orm import Session
from app.db.models import plead_offers, plead_contracts, plead_transactions, plead_user_connections
from datetime import datetime
from app.opensearch.creatre_contract import generate_contract
from app.opensearch.opensearch_client import  create_opensearch_client, create_single_document, create_index
from app.api.v1.agreements.constant import DB_QUERIES
from app.blockchain.interact import create_transaction
from app.db.models import User
from app.api.v1.auth.utility import get_public_key
import uuid
import json
DEFAULT_RATE = 10
INDEX_NAME = "contracts_v2"

router = APIRouter()

class OfferStatus(str, Enum):
    pending = "pending"
    countered = "countered"
    accepted = "accepted"
    rejected = "rejected"
    not_pending = "not_pending"

class AcceptOfferRequest(BaseModel):
    offerId: str
    offerDetails: str
    contractType: str
    senderId: int
    contract_title: str
    privateKey: str

@router.post("/accept-offer")
async def send_offer(
    request: AcceptOfferRequest,
    db: Session = Depends(get_db_connection),
    current_user: str = Depends(get_current_user)  # Automatically gets the current user from the JWT token
):
    print(f"Current user: {current_user}")
    offer_id = request.offerId
    offer_details = request.offerDetails
    print(f"Offer details: {offer_details}")
    # def get_user_details(user_id):
    #     return db.query(User).filter(User.id == user_id).first()
    contract_id = uuid.uuid4()
    get_user_details = lambda user_id: db.query(User).filter(User.id == user_id).first()
    if request.contractType != "CUSTOM CONTRACT":
        import re
        offer_details =  re.sub(r"'", '"', offer_details)
        offer_details = json.loads(offer_details)
    # (agreement_type, agreement_name, date, party1_name, party1_address, party2_name, party2_address,
    #                   amount=None, rate=None, duration=None, payment_mode=None, repayment_type=None, penalty=None,
    #                   days=None, city=None, jurisdiction=None, product_name=None, quantity=None, price_per_unit=None,
    #                   total_price=None, delivery_days=None, service_name=None, completion_deadline=None, commodity_name=None,
    #                   amount_sent=None, currency_sent=None, converted_amount=None, currency_received=None, exchange_rate=None,
    #                   interest_rate=None, late_interest_rate=None, repayment_due_date=None,party1_contact=None,party2_contact=None)  
    #  
    else:
        document = {
            "contract_id": contract_id,
            "contract_type": request.contractType,
            "contract_title": request.contract_title,
            "contract_data": offer_details
        }
    if request.contractType == "LOAN AGREEMENT":
        document = generate_contract(contract_id=contract_id,agreement_type=request.contractType,agreement_name= request.contract_title,date= datetime.utcnow(),party1_name=get_user_details(request.senderId).name,party1_address=get_user_details(request.senderId).address,party2_name=get_user_details(current_user).name,party2_address=get_user_details(current_user).address,amount=offer_details.amount,payment_mode=offer_details.payment_mode,repayment_type=offer_details.repayment_type,interest_rate=offer_details.get('interest_rate',DEFAULT_RATE),rate=DEFAULT_RATE,repayment_due_date=offer_details.get('repayment_due_date'))
    elif request.contractType == "FRIENDLY LOAN AGREEMENT":
        document = generate_contract(contract_id=contract_id,agreement_type=request.contractType,agreement_name= request.contract_title,date= datetime.utcnow(),party1_name=get_user_details(request.senderId).name,party1_address=get_user_details(request.senderId).address,party2_name=get_user_details(current_user).name,party2_address=get_user_details(current_user).address,amount=offer_details.amount,payment_mode=offer_details.payment_mode,repayment_type=offer_details.repayment_type,interest_rate=offer_details.get('interest_rate',DEFAULT_RATE),rate=DEFAULT_RATE,repayment_due_date=offer_details.get('repayment_due_date'))
    elif request.contractType == "SALES AGREEMENT":
        document = generate_contract(contract_id=contract_id,agreement_type=request.contractType,agreement_name= request.contract_title,date= datetime.utcnow(),party1_name=get_user_details(request.senderId).name,party1_address=get_user_details(request.senderId).address,party2_name=get_user_details(current_user).name,party2_address=get_user_details(current_user).address,amount=offer_details.amount,payment_mode=offer_details.payment_mode,repayment_type=offer_details.repayment_type,interest_rate=offer_details.get('interest_rate',DEFAULT_RATE),rate=DEFAULT_RATE,repayment_due_date=offer_details.get('repayment_due_date'))
    elif request.contractType == "CURRENCY EXCHANGE AGREEMENT":
        document = generate_contract(contract_id=contract_id,agreement_type=request.contractType,agreement_name= request.contract_title,date= datetime.utcnow(),party1_name=get_user_details(request.senderId).name,party1_address=get_user_details(request.senderId).address,party2_name=get_user_details(current_user).name,party2_address=get_user_details(current_user).address,amount=offer_details.amount,payment_mode=offer_details.payment_mode,repayment_type=offer_details.repayment_type,interest_rate=offer_details.get('interest_rate',DEFAULT_RATE),rate=DEFAULT_RATE,repayment_due_date=offer_details.get('repayment_due_date'))
    elif request.contractType == "BARTER AGREEMENT":
        document = generate_contract(contract_id=contract_id,agreement_type=request.contractType,agreement_name= request.contract_title,date= datetime.utcnow(),party1_name=get_user_details(request.senderId).name,party1_address=get_user_details(request.senderId).address,party2_name=get_user_details(current_user).name,party2_address=get_user_details(current_user).address,amount=offer_details.amount,payment_mode=offer_details.payment_mode,repayment_type=offer_details.repayment_type,interest_rate=offer_details.get('interest_rate',DEFAULT_RATE),rate=DEFAULT_RATE,repayment_due_date=offer_details.get('repayment_due_date'))

    print(f"Document: {document}")
    client = create_opensearch_client()
    create_index(client,INDEX_NAME)
    create_single_document(client,INDEX_NAME,document)

    if not offer_id :
        raise HTTPException(status_code=400, detail="Offer ID and User ID are required.")


    try:
        print(f"Accepting offer with ID: {offer_id} for user ID: {current_user}")

        
        # Step 1: Create an entry in the blockchain
            #  = await create_blockchain_entry(offer_id, user_id)  # Hypothetical function to interact with the blockchain
        # transaction_hash = create_transaction(get_public_key(current_user)[0], get_public_key(request.senderId)[0], document, private_key=request.privateKey)
        transaction_hash = create_transaction(recipient=get_public_key(request.senderId)[0],sender=get_public_key(current_user)[0],contract_details=document,private_key=request.privateKey)
        # Step 2: Create an entry in plead_contracts
        # connection = db.query(plead_user_connections).filter(
        #     plead_user_connections.user_id == user_id
        # ).first()
        # print(f"Connection: {connection}")

        # if not connection:
        #     raise HTTPException(status_code=404, detail="Connection not found.")

        try:
            new_contract = plead_contracts(
                contract_id = contract_id,
                sender_id = request.senderId,
                receiver_id = current_user,
                contract_data = document.get('summary','Not provided'),
                contract_status = 'accepted',
                transaction_hash = transaction_hash,
                contract_title = request.contract_title,
                contract_type = request.contractType,
                created_at = datetime.utcnow()
            )

            db.add(new_contract)
            db.commit()
            db.refresh(new_contract)
            print(f"New contract created: {new_contract.contract_id}")
        except Exception as e:
            print(f"Error creating new contract: {e}")
            raise HTTPException(status_code=500, detail="Internal server error.")
        
    
        new_offer = plead_offers(       
            offer_id = uuid.uuid4(),
            contract_id = contract_id,
            sender_id = request.senderId,
            receiver_id = current_user,
            offer_details = offer_details,
            offer_status = 'accepted',
            counter_offer_id = None,
            created_at = datetime.utcnow(),
            contract_type = request.contractType,
            sender_public_key = get_public_key(request.senderId)[0],
            receiver_public_key = get_public_key(current_user)[0],
            contract_title = request.contract_title

        )

        db.add(new_offer)
        db.commit()
        db.refresh(new_offer)
        print(f"New offer created: {new_offer.offer_id}")
        # update_offer = db.query(plead_offers).filter(
        #     plead_offers.offer_id == offer_id).update(
        #     {
        #        'contract_id': new_contract.contract_id,
        #        'offer_status': OfferStatus.not_pending
        #     }
        # )
        # db.commit()
        # db.refresh(update_offer)
        # print(f"Offer updated: {update_offer.offer_id}")


# class plead_offers(Base):
#     __tablename__ = 'plead_offers'

#     offer_id = Column(UUID, primary_key=True, default=uuid.uuid4)
#     contract_id = Column(UUID, ForeignKey('plead_contracts.contract_id'), nullable=False)
#     sender_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
#     receiver_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
#     offer_details = Column(String, nullable=False)
#     offer_status = Column(String, nullable=False)
#     counter_offer_id = Column(UUID, ForeignKey('plead_offers.offer_id'), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     contract_type = Column(String, nullable=False)
#     sender_public_key = Column(String, nullable=False)
#     receiver_public_key = Column(String, nullable=False)
#     contract_title = Column(String, nullable=False)
        print(f"Request: {uuid.UUID(request.offerId)}",request.offerId, OfferStatus.not_pending, type(OfferStatus.not_pending), type(request.offerId))
        update_offer = db.query(plead_offers).filter(
            plead_offers.offer_id == uuid.UUID(request.offerId)
        ).first()
        update_offer.offer_status = OfferStatus.not_pending
        db.commit()

        # db.commit()
        # db.refresh(update_offer)
        print(f"Offer updated: {update_offer}")
        # new_transaction = plead_transactions(
        #     transaction_id = None,
        #     contract_id = new_contract.contract_id,
        #     arbitrator_id = None,
        #     sender_legal_counsel_id = None,
        #     receiver_legal_counsel_id = None,
        #     sender_legal_counsel_type = 'active',
        #     receiver_legal_counsel_type = 'active',
        #     transaction_status = 'pending'  
        # )
        # db.add(new_transaction)
        # db.commit()
        # db.refresh(new_transaction)
    
        return {"message": "Offer accepted successfully!",
                "contract_id": new_contract.contract_id}

    except Exception as e:
        print('Error accepting offer:', e)
        raise HTTPException(status_code=500, detail="Internal server error.")
