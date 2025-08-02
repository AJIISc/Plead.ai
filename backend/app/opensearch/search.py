from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from opensearchpy import OpenSearch
import json

router = APIRouter()

# Load configuration from config.json
def load_config(config_file='config.ini'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

# Create an OpenSearch client
def create_opensearch_client(config):
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']

    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=(username, password),
        use_ssl=False,
        verify_certs=False
    )
    return client

# Define a request model
class SearchRequest(BaseModel):
    index: str
    key: str

# API endpoint to search documents
@router.post("/search")
async def search_documents(request: SearchRequest):
    config = load_config()
    client = create_opensearch_client(config)

    # Construct the search query
    query = {
        "query": {
            "match": {
                "content": request.key  # Assuming you are searching in the 'content' field
            }
        }
    }

    # Perform the search
    try:
        response = client.search(index=request.index, body=query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Extract the documents from the response
    documents = [hit['_source'] for hit in response['hits']['hits']]

    return {"documents": documents}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(router, host='0.0.0.0', port=9300)