from web3 import Web3

# Connect to Ganache (or any Ethereum node)
ganache_url = "http://127.0.0.1:7545"  # Default Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connected
if not web3.is_connected:
    print("Failed to connect to Ganache")
    exit()

print("Connected to Ganache")

# Function to create a new Ethereum account
def create_account():
    # Create a new account
    account = web3.eth.account.create()

    # Display the account details
    print("New Account Address:", account.address)
    print("New Account Private Key:", account._private_key.hex())  # Display private key in hex format

    return account.address, account._private_key.hex()

# Example usage
if __name__ == "__main__":
    create_account()