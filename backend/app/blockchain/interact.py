from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connected
if not web3.is_connected:
    print("Failed to connect to Ganache")
    exit()

print("Connected to Ganache")

# Get accounts from Ganache
accounts = web3.eth.accounts
print("Accounts:", accounts)

# Function to create a transaction
def create_transaction(sender, recipient, contract_details,amount=0.1,private_key=None):
    # Convert amount to Wei (1 Ether = 10^18 Wei)
    amount_in_wei = web3.to_wei(amount, 'ether')
    # contract_data = json.dumps(contract_details)
    encoded_data = web3.to_hex(text=str(contract_details)) 
    print(f"Encoded data: {encoded_data}",sender,type(sender),type(recipient))
    # Create a transaction
    transaction = {
        'to': recipient,
        'value': amount_in_wei,
        'gas': 2000000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'nonce': web3.eth.get_transaction_count(str(sender)),
        'data': encoded_data
    }

    # Sign the transaction
    print(f"Private key: {str(private_key)}")
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction sent! Hash: {web3.to_hex(txn_hash)}")
    return web3.to_hex(txn_hash)

# Example usage
if __name__ == "__main__":
    sender_account = "0xbf514b3BBAA9BD3Be5fA98A80274D07a787CA38C"
    recipient_account = "0x6fdd494E1Ba695EAD3aCaE2e0B201B62C9C9100b"  # Use the second account
    amount_to_send = 10  # Amount in Ether

    contract_details = {
        'contract_id': '1234567890',
        'contract_type': 'Plead',
        'contract_status': 'Pending',
        'contract_details': 'This is a test contract'
    }
    create_transaction(sender_account, recipient_account, amount=amount_to_send, contract_details=contract_details)
    balance = web3.eth.get_balance(recipient_account)
    print("New Wallet Balance:", web3.from_wei(balance, 'ether'), "ETH")

#     New Account Address: 0xa7f9d6C89f05C3BF705983c21F70217E8CF7792b
# New Account Private Key: 48c654e5855e9b972d2f6e61686b8443dbf506cc41a6c1de7def42ea19c6fd5c