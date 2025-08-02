
CREATE TABLE plead_user_information (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    address TEXT,
    user_type VARCHAR(20) NOT NULL, 
    role VARCHAR(20) NOT NULL ,
    public_key VARCHAR(100) NOT NULL,
    private_key VARCHAR(100) NOT NULL
);
CREATE TABLE plead_user_login (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES plead_user_information(id),
    user_type VARCHAR(20) NOT NULL,  -- individual or enterprise
    role VARCHAR(20) NOT NULL,       -- customer, legal counsel, arbitrator
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP
);
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE plead_contracts (
    contract_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id INTEGER REFERENCES plead_user_information(id) ON DELETE SET NULL,
    receiver_id INTEGER REFERENCES plead_user_information(id) ON DELETE SET NULL,
    contract_data TEXT NOT NULL,
    contract_status TEXT CHECK (contract_status IN ('draft', 'accepted', 'breached','disputed', 'executed','terminated')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contract_title TEXT NOT NULL,
    contract_type TEXT CHECK  NOT NULL
);

CREATE TABLE plead_transactions (
    contract_id UUID REFERENCES plead_contracts(contract_id) ON DELETE CASCADE,
    arbitrator_id INTEGER REFERENCES plead_user_information(id) ON DELETE SET NULL,
    sender_legal_counsel_id INTEGER REFERENCES plead_user_information(id) ON DELETE SET NULL,
    receiver_legal_counsel_id INTEGER REFERENCES plead_user_information(id) ON DELETE SET NULL,
    sender_legal_counsel_type TEXT CHECK (sender_legal_counsel_type IN ('active', 'passive')) NOT NULL,
    receiver_legal_counsel_type TEXT CHECK (receiver_legal_counsel_type IN ('active', 'passive')) NOT NULL,
    transaction_status TEXT CHECK (transaction_status IN ('active','pending', 'completed', 'disputed')) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plead_blockchain (
    block_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID REFERENCES plead_contracts(contract_id) ON DELETE CASCADE,
    sender_public_key TEXT NOT NULL,
    receiver_public_key TEXT NOT NULL,
    contract_data_hash TEXT NOT NULL,
    transaction_hash TEXT NOT NULL,
    block_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE plead_user_connections (
    id SERIAL PRIMARY KEY,
    user_id SERIAL NOT NULL REFERENCES plead_user_information(id) ON DELETE CASCADE,
    connection_id SERIAL NOT NULL REFERENCES plead_user_information(id) ON DELETE CASCADE,
    user_public_key TEXT NOT NULL,
    connection_public_key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, connection_id)
);

CREATE TYPE offer_status AS ENUM ('pending', 'countered', 'accepted', 'rejected','not_pending');

CREATE TABLE plead_offers (
    offer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID REFERENCES plead_contracts(contract_id) ON DELETE CASCADE,
    contract_type TEXT NOT NULL,
    sender_id Integer REFERENCES plead_user_information(id) ON DELETE SET NULL,
    sender_public_key TEXT NOT NULL,
    receiver_id Integer REFERENCES plead_user_information(id) ON DELETE SET NULL,
    receiver_public_key TEXT NOT NULL,
    offer_details TEXT NOT NULL,
    offer_status offer_status NOT NULL,  
    counter_offer_id UUID REFERENCES plead_offers(offer_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
