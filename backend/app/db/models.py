from sqlalchemy import Column, ForeignKey, String, DateTime, Integer, UUID
from sqlalchemy.orm import relationship
from app.db.database import Base  # Adjust based on your actual database setup
from datetime import datetime
import uuid


    
class plead_user_connections(Base):
    __tablename__ = 'plead_user_connections'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
    connection_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", foreign_keys=[user_id])
    connection = relationship("User", foreign_keys=[connection_id])
    user_public_key = Column(String, nullable=False)
    connection_public_key = Column(String, nullable=False)


class plead_contracts(Base):
    __tablename__ = 'plead_contracts'

    contract_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    sender_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
    contract_data = Column(String, nullable=False)
    contract_status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    contract_title = Column(String, nullable=False)
    contract_type = Column(String, nullable=False)
    transaction_hash = Column(String, nullable=False)


class plead_offers(Base):
    __tablename__ = 'plead_offers'

    offer_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID, ForeignKey('plead_contracts.contract_id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=False)
    offer_details = Column(String, nullable=False)
    offer_status = Column(String, nullable=False)
    counter_offer_id = Column(UUID, ForeignKey('plead_offers.offer_id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    contract_type = Column(String, nullable=False)
    sender_public_key = Column(String, nullable=False)
    receiver_public_key = Column(String, nullable=False)
    contract_title = Column(String, nullable=False)


class plead_transactions(Base):
    __tablename__ = 'plead_transactions'

    transaction_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID, ForeignKey('plead_contracts.contract_id'), nullable=False)
    arbitrator_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=True)
    sender_legal_counsel_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=True)
    receiver_legal_counsel_id = Column(Integer, ForeignKey('plead_user_information.id'), nullable=True)
    sender_legal_counsel_type = Column(String, nullable=False)
    receiver_legal_counsel_type = Column(String, nullable=False)
    transaction_status = Column(String, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    transaction_hash = Column(String, nullable=False)
    contract_type = Column(String, nullable=False)
    contract_title = Column(String, nullable=False)


class plead_blockchain(Base):
    __tablename__ = 'plead_blockchain'

    block_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID, ForeignKey('plead_contracts.contract_id'), nullable=False)
    sender_public_key = Column(String, nullable=False)
    receiver_public_key = Column(String, nullable=False)
    contract_data_hash = Column(String, nullable=False)
    transaction_hash = Column(String, nullable=False)
    block_timestamp = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'plead_user_information'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    role = Column(String, nullable=False)
    public_key = Column(String, nullable=False)
    private_key = Column(String, nullable=False)

    def verify_password(self, password):
        return self.password == password

    

