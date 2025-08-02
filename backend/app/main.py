from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth.signup import router as signup_router
from app.api.v1.auth.connections import router as connections_router
from app.api.v1.auth.auth import router as auth_router
from app.api.v1.agreements.offers import router as offers_router
from app.api.v1.agreements.agreement import router as agreement_router
from app.opensearch.search import router as opensearch_router
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the signup router
app.include_router(signup_router, prefix="/api/v1")
app.include_router(connections_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(offers_router, prefix="/api/v1")
app.include_router(agreement_router, prefix="/api/v1")
app.include_router(opensearch_router, prefix="/api/v1/opensearch")

@app.get("/")
async def root():
    return {"message": "Hello PleadAI"}