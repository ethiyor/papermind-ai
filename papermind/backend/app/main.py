from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv


from .pdf_utils import extract_text_from_pdf
from .embed_utils import chunk_text, embed_chunks, search_chunks
try:
    from .summarizer_utils import summarize_text, get_available_models
    ML_AVAILABLE = True
except ImportError:
    from .minimal_summarizer import summarize_text_minimal as summarize_text
    ML_AVAILABLE = False
    def get_available_models():
        return {"minimal": "rule-based extractive summarizer"}

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    # Try loading from parent directory
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print("Loaded SUPABASE_URL:", SUPABASE_URL)
print("Loaded SUPABASE_KEY:", SUPABASE_KEY[:5] + "..." if SUPABASE_KEY else "None")

# Initialize Supabase client with error handling
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
        supabase = None
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment variables")
    print("Please create a .env file with your Supabase credentials")

# Initialize FastAPI app
app = FastAPI(
    title="PaperMind AI API",
    description="AI-powered PDF analysis and summarization API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for production
origins = [
    "http://localhost:3000",
    "http://localhost:8080", 
    "http://127.0.0.1:8080",
    "https://*.onrender.com",  # Render domains
    "https://papermind-ai-frontend-pnbb.onrender.com",  # Your deployed frontend
    "https://papermind-ai-backend-lpqr.onrender.com",  # Your deployed backend
    "https://papermind-ai-frontend-production.up.railway.app",  # Railway frontend
    "https://papermind-ai-production.up.railway.app",  # Railway backend
    # Add your frontend domain here when deployed
]

# For development, allow all origins
import os
if os.getenv("ENVIRONMENT") != "production":
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to PaperMind AI API!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "upload": "/upload-pdf/",
            "search": "/search/",
            "summarize": "/summarize/",
            "models": "/models/"
        }
    }

# Health check endpoint for monitoring
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-09-05",
        "service": "PaperMind AI Backend",
        "version": "1.0.0"
    }

# In-memory fallback storage
stored_chunks = []
stored_embeddings = None

# Pydantic schemas
class SummarizeRequest(BaseModel):
    text: str
    model: Optional[str] = "bart"  # Default model
    style: Optional[str] = "academic"  # academic, brief, detailed
    chunk_length: Optional[int] = 1000

from typing import Optional

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global stored_chunks, stored_embeddings

    # Read and extract text
    contents = await file.read()
    print(f"PDF file size: {len(contents)} bytes")
    
    text = extract_text_from_pdf(contents)
    print(f"Extracted text length: {len(text)}")
    print(f"Extracted text preview: {repr(text[:200])}")
    
    stored_chunks = chunk_text(text)
    print(f"Number of chunks created: {len(stored_chunks)}")
    
    if stored_chunks:
        stored_embeddings = embed_chunks(stored_chunks)
        print("Embeddings created successfully")
    else:
        stored_embeddings = None
        print("No chunks to embed")

    pdf_id = None
    
    # Only use Supabase if client is available
    if supabase:
        # Upload file to Supabase Storage
        storage_path = f"pdfs/{file.filename}"
        try:
            supabase.storage.from_("papers").upload(
                path=storage_path,
                file=contents,
                file_options={"content-type": file.content_type}
            )
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Upload failed: {str(e)}"})

        # Store PDF metadata
        pdf_resp = supabase.table("pdfs").insert({
            "title": file.filename,
            "storage_path": storage_path,
        }).execute()

        pdf_id = pdf_resp.data[0]['id'] if pdf_resp.data else None

        # Save chunks
        for i, chunk in enumerate(stored_chunks):
            supabase.table("chunks").insert({
                "pdf_id": pdf_id,
                "chunk_index": i,
                "content": chunk
            }).execute()
    else:
        print("Supabase not available - storing chunks in memory only")

    return {
        "message": f"{len(stored_chunks)} chunks embedded and stored.",
        "preview": stored_chunks[:2],
        "pdf_id": pdf_id,
        "supabase_available": supabase is not None
    }

@app.post("/search/")
async def semantic_search(query: str = Form(...)):
    if not stored_chunks or stored_embeddings is None:
        return {"error": "No PDF uploaded yet."}

    results = search_chunks(query, stored_chunks, stored_embeddings)
    return {"results": results}

@app.post("/summarize/")
async def summarize_local(data: SummarizeRequest):
    text = data.text
    if not text:
        return JSONResponse(status_code=400, content={"error": "No text provided."})

    try:
        summary = summarize_text(
            text, 
            max_chunk_length=data.chunk_length,
            model=data.model,
            style=data.style
        )
        return {
            "summary": summary,
            "model_used": data.model,
            "style": data.style
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/models/")
async def get_models():
    """Get available summarization models"""
    return {
        "available_models": get_available_models(),
        "styles": ["academic", "brief", "detailed"]
    }
