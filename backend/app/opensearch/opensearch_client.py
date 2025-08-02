import json
from opensearchpy import OpenSearch, RequestsHttpConnection

# Load configuration from config.json
def load_config(config_file='config.ini'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

# Create an OpenSearch client
def create_opensearch_client():
    config = load_config('app/opensearch/config.ini')
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']

    # Create the OpenSearch client
    print("Creating OpenSearch client")
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],  # Use the correct port from config
        http_auth=(username, password),
        use_ssl=False,
        verify_certs=False,
    )
    print("OpenSearch client created")
    return client

# Create an index
def create_index(client,index_name):

    print("Creating index")
    if not client.indices.exists(index=index_name):
        response = client.indices.create(index=index_name)
        print(f"Index '{index_name}' created: {response}")
    else:
        print(f"Index '{index_name}' already exists.")

# Add a single document to the index
def create_single_document(client, index_name, document):

    doc_id = document.get("contract_id", None)  # Use contract_id as the document ID
    response = client.index(index=index_name, id=doc_id, body=document)
    print(f"Document added to index '{index_name}': {response}")

def create_multiple_documents(client, index_name, documents):
    for document in documents:
        create_single_document(client, index_name, document)


# Search for contracts based on criteria
def search_contracts(client, index_name, search_criteria):
    query = {
        "query": {
            "bool": {
                "must": []
            }
        }
    }

    # Add search criteria to the query
    for key, value in search_criteria.items():
        query["query"]["bool"]["must"].append({"match": {key: value}})

    response = client.search(index=index_name, body=query)
    return response['hits']['hits']

# Read documents from the index
def read_documents(client, index_name):
    response = client.search(index=index_name, body={"query": {"match_all": {}}})
    return response['hits']['hits']

# Example usage
if __name__ == "__main__":
    config = load_config()
    print(config)
    client = create_opensearch_client(config)

    # Create an index
    create_index(client, config['index'])

    # Example document to add
    document = {
        "contract_id": "C001",
        "contract_type": "Online Payment for Lending",
        "parties": [
            {"name": "Party A", "role": "Lender", "contact": "lender@email.com"},
            {"name": "Party B", "role": "Borrower", "contact": "borrower@email.com"}
        ],
        "jurisdiction": "India",
        "governing_law": "Indian Contract Act, 1872",
        "validity_period": {"start_date": "2024-03-22", "end_date": "2025-03-22"},
        "transaction_details": {
            "amount": "₹1,00,000",
            "currency": "INR",
            "payment_mode": "Online Transfer",
            "payment_terms": "Full payment upfront",
            "interest_rate": "10% per annum",
            "due_date": "2024-12-31"
        },
        "delivery_terms": {
            "mode": "Instant Transfer",
            "conditions": "Funds must be available in Borrower’s account within 24 hours."
        },
        "clauses": [
            {
                "clause_id": "C001_001",
                "title": "Payment Terms",
                "text": "The Borrower agrees to repay the Lender the principal amount of ₹1,00,000 with an interest of 10% per annum by December 31, 2024."
            },
            {
                "clause_id": "C001_002",
                "title": "Dispute Resolution",
                "text": "Any dispute arising shall be resolved through arbitration under the Arbitration and Conciliation Act, 1996."
            }
        ],
        "summary": "A loan agreement between Party A and Party B for ₹1,00,000 at 10% interest.",
        "tags": ["Lending", "Online Payment", "Loan Agreement"]
    }

    # Add a single document to the index
    create_single_document(client, config['index'], document)

    # Search for contracts
    search_criteria = {
        "contract_id": "C001"  # Example search criteria
    }
    found_contracts = search_contracts(client, config['index'], search_criteria)
    print("Found contracts:")
    for contract in found_contracts:
        print(contract['_source'])

    # Read documents from the index
    print("Reading all documents")
    documents = read_documents(client, config['index'])
    print("Documents in index:")
    for doc in documents:
        print(doc['_source'])