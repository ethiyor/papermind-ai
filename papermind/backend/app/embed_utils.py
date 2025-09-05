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
    if not text or not text.strip():
        return []
    
    # Clean up the text
    text = text.strip()
    
    # Split by sentences first, then by lines
    sentences = text.replace('\n', ' ').split('. ')
    chunks, current = [], ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Add period back if it was removed by split
        if not sentence.endswith('.') and not sentence.endswith('!') and not sentence.endswith('?'):
            sentence += '.'
            
        if len(current) + len(sentence) + 1 < max_length:
            current += " " + sentence if current else sentence
        else:
            if current:
                chunks.append(current.strip())
            current = sentence
    
    if current:
        chunks.append(current.strip())

    # Filter out empty chunks and ensure minimum length
    return [c for c in chunks if c and len(c.strip()) > 10]


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
