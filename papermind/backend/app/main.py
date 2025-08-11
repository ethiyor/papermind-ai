from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

from app.pdf_utils import extract_text_from_pdf
from app.embed_utils import chunk_text, embed_chunks, search_chunks
from app.summarizer_utils import summarize_text

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print("Loaded SUPABASE_URL:", SUPABASE_URL)
print("Loaded SUPABASE_KEY:", SUPABASE_KEY[:5] + "..." if SUPABASE_KEY else "None")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI app
app = FastAPI()

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory fallback storage
stored_chunks = []
stored_embeddings = None

# Pydantic schema for summarization input
class SummarizeRequest(BaseModel):
    text: str

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global stored_chunks, stored_embeddings

    # Read and extract text
    contents = await file.read()
    text = extract_text_from_pdf(contents)
    stored_chunks = chunk_text(text)
    stored_embeddings = embed_chunks(stored_chunks)

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

    return {
        "message": f"{len(stored_chunks)} chunks embedded and stored.",
        "preview": stored_chunks[:2],
        "pdf_id": pdf_id
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
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
