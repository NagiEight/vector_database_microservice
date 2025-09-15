from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vector_db import VectorDatabase
from sentence_transformers import SentenceTransformer
from waitress import serve # Add this line

# Initialize FastAPI and the components
app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
db = VectorDatabase(dimension=model.get_sentence_embedding_dimension())

# Configure CORS middleware to allow requests from the web GUI
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request validation
class AddVectorsRequest(BaseModel):
    texts: list[str]
    metadata: list[dict]

class SearchVectorsRequest(BaseModel):
    query: str
    k: int = 5

@app.post("/vectors/add")
def add_vectors(request: AddVectorsRequest):
    """Adds new vectors and their metadata."""
    if len(request.texts) != len(request.metadata):
        raise HTTPException(status_code=400, detail="Texts and metadata must have the same length.")
    ids = db.add(request.texts, request.metadata)
    return {"status": "success", "ids": ids}

@app.post("/vectors/search")
def search_vectors(request: SearchVectorsRequest):
    """Performs a similarity search."""
    results = db.search(request.query, request.k)
    return {"results": results}

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# Add the following to make it runnable by run.py
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)