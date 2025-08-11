from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_model = None  # Lazy-loaded model


def get_model():
    """Load the model only once, on demand."""
    global _model
    if _model is None:
        print("Loading SentenceTransformer model (this may take a bit)...")
        _model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    return _model


# Split text into manageable chunks
def chunk_text(text: str, max_length: int = 500) -> list:
    lines = text.split("\n")
    chunks, current = [], ""

    for line in lines:
        if len(current) + len(line) < max_length:
            current += " " + line.strip()
        else:
            chunks.append(current.strip())
            current = line.strip()
    if current:
        chunks.append(current.strip())

    return [c for c in chunks if c]


# Embed a list of text chunks
def embed_chunks(chunks: list[str]) -> np.ndarray:
    model = get_model()
    return model.encode(chunks)


# Perform semantic search over embedded chunks
def search_chunks(query: str, chunks: list[str], embeddings: np.ndarray, top_k: int = 3) -> list[str]:
    model = get_model()
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = scores.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]
