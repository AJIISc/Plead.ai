import hashlib
import json
import requests

BLOCKCHAIN_URL = "http://your-blockchain-node-url"  # Replace with your actual blockchain node URL

def create_blockchain_entry(offer_id: str, user_id: int) -> str:
    # Validate inputs
    if not isinstance(offer_id, str) or not isinstance(user_id, int):
        raise ValueError("Invalid input types for offer_id or user_id.")

    # Create the transaction data
    transaction_data = {
        "offer_id": offer_id,
        "user_id": user_id,
        "timestamp": get_current_timestamp()  # Function to get the current timestamp
    }

    # Hash the transaction data for integrity
    transaction_hash = hashlib.sha256(json.dumps(transaction_data).encode()).hexdigest()
    transaction_data["hash"] = transaction_hash

    # Send the transaction to the blockchain
    try:
        response = requests.post(f"{BLOCKCHAIN_URL}/transactions", json=transaction_data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get("transaction_hash")  # Assuming the blockchain returns the transaction hash
    except requests.exceptions.RequestException as e:
        print(f"Error sending transaction to blockchain: {e}")
        raise Exception("Failed to create blockchain entry.")

def get_current_timestamp() -> str:
    from datetime import datetime
    return datetime.utcnow().isoformat() 