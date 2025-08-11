# app/summarizer_utils.py

from transformers import pipeline

# Load local summarization pipeline (first time downloads model)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str, max_chunk_length=1000):
    """Splits long text and summarizes in pieces"""
    summaries = []

    # Split text into chunks that fit within model limits
    for i in range(0, len(text), max_chunk_length):
        chunk = text[i:i + max_chunk_length]
        summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    return " ".join(summaries)
