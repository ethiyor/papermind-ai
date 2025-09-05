# app/summarizer_utils.py

from transformers import pipeline
import re
from typing import List, Optional

class PaperMindSummarizer:
    """Advanced summarization with multiple model options for academic papers"""
    
    def __init__(self, model_name: str = "t5-small"):
        """Initialize with specified model"""
        self.model_name = model_name
        self.summarizer = None
        self.load_model()
    
    def load_model(self):
        """Load the summarization model"""
        try:
            print(f"Loading summarization model: {self.model_name}")
            self.summarizer = pipeline("summarization", model=self.model_name)
            print("✓ Summarization model loaded successfully")
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            # Fallback to ultra-lightweight T5
            print("Falling back to ultra-lightweight T5-small model...")
            self.model_name = "t5-small"
            self.summarizer = pipeline("summarization", model=self.model_name)
    
    def preprocess_academic_text(self, text: str) -> str:
        """Preprocess text specifically for academic papers"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common academic paper artifacts
        text = re.sub(r'\b(Figure|Table|Fig\.|Tab\.)\s+\d+[^\n]*', '', text)
        text = re.sub(r'\[\d+\]', '', text)  # Remove reference citations
        text = re.sub(r'\b(et al\.)', 'and colleagues', text)
        
        # Remove URLs and DOIs
        text = re.sub(r'http[s]?://\S+', '', text)
        text = re.sub(r'doi:\S+', '', text)
        
        return text.strip()
    
    def smart_chunk_text(self, text: str, max_length: int = 1000) -> List[str]:
        """Intelligently chunk text preserving sentence boundaries"""
        # First preprocess the text
        text = self.preprocess_academic_text(text)
        
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence would exceed the limit
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Filter out very short chunks
        return [chunk for chunk in chunks if len(chunk.split()) >= 10]
    
    def summarize_text(self, text: str, max_chunk_length: int = 1000, 
                      summary_style: str = "academic") -> str:
        """Advanced text summarization with different styles"""
        if not text.strip():
            return "No text provided for summarization."
        
        chunks = self.smart_chunk_text(text, max_chunk_length)
        
        if not chunks:
            return "Text too short for meaningful summarization."
        
        summaries = []
        
        # Adjust parameters based on summary style
        if summary_style == "academic":
            max_length = min(150, len(text.split()) // 3)
            min_length = min(50, max_length // 3)
        elif summary_style == "brief":
            max_length = min(100, len(text.split()) // 4)
            min_length = min(30, max_length // 3)
        else:  # detailed
            max_length = min(200, len(text.split()) // 2)
            min_length = min(80, max_length // 3)
        
        for i, chunk in enumerate(chunks):
            try:
                # Adjust max_length if chunk is very short
                chunk_words = len(chunk.split())
                chunk_max_length = min(max_length, chunk_words // 2) if chunk_words < 100 else max_length
                chunk_min_length = min(min_length, chunk_max_length // 2)
                
                if chunk_max_length < 10:
                    # Skip very short chunks or add them directly
                    summaries.append(chunk[:200])
                    continue
                
                # Handle T5 models which need text preprocessing
                if "t5" in self.model_name.lower():
                    # T5 expects "summarize: " prefix
                    input_text = f"summarize: {chunk}"
                else:
                    input_text = chunk
                
                summary = self.summarizer(
                    input_text,
                    max_length=chunk_max_length,
                    min_length=chunk_min_length,
                    do_sample=False,
                    truncation=True
                )[0]['summary_text']
                
                summaries.append(summary)
                
            except Exception as e:
                print(f"Error summarizing chunk {i+1}: {e}")
                # Fallback: use first few sentences of the chunk
                sentences = chunk.split('. ')
                fallback = '. '.join(sentences[:3]) + '.'
                summaries.append(fallback)
        
        # Combine summaries intelligently
        final_summary = self.combine_summaries(summaries)
        return final_summary
    
    def combine_summaries(self, summaries: List[str]) -> str:
        """Intelligently combine multiple summaries"""
        if not summaries:
            return "No summary could be generated."
        
        if len(summaries) == 1:
            return summaries[0]
        
        # Join summaries with appropriate transitions
        combined = summaries[0]
        
        for i, summary in enumerate(summaries[1:], 1):
            if i == len(summaries) - 1:
                combined += f" Finally, {summary.lower()}"
            else:
                combined += f" Additionally, {summary.lower()}"
        
        return combined
    
    def switch_model(self, new_model: str):
        """Switch to a different summarization model"""
        self.model_name = new_model
        self.load_model()

# Available models for different use cases (ultra-lightweight for 512MB)
AVAILABLE_MODELS = {
    "t5": "t5-small",                               # Ultra-lightweight ~60MB (RECOMMENDED for free tier)
    "distilbart": "sshleifer/distilbart-cnn-6-6",  # Lightweight ~268MB (may hit memory limit)
    "bart": "sshleifer/distilbart-cnn-12-6",       # Medium ~600MB (likely to exceed memory)
    "pegasus": "google/pegasus-xsum",              # News-style (large - exceeds memory)
    "led": "allenai/led-base-16384",               # For long docs (very large - exceeds memory)
}

# Initialize default summarizer
_default_summarizer = PaperMindSummarizer()

def summarize_text(text: str, max_chunk_length: int = 1000, 
                  model: str = "t5", style: str = "academic") -> str:
    """Main summarization function with model selection"""
    global _default_summarizer
    
    # Switch model if requested
    if model in AVAILABLE_MODELS and _default_summarizer.model_name != AVAILABLE_MODELS[model]:
        _default_summarizer.switch_model(AVAILABLE_MODELS[model])
    
    return _default_summarizer.summarize_text(text, max_chunk_length, style)

def get_available_models() -> dict:
    """Return available summarization models"""
    return AVAILABLE_MODELS
