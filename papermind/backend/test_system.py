#!/usr/bin/env python3
"""
Test script to verify PaperMind dependencies and functionality
"""
import sys
import os

def test_imports():
    """Test all required imports"""
    try:
        print("Testing imports...")
        
        # Basic imports
        from fastapi import FastAPI
        print("✓ FastAPI imported")
        
        from pdfminer.high_level import extract_text
        print("✓ PDFMiner imported")
        
        from sentence_transformers import SentenceTransformer
        print("✓ SentenceTransformers imported")
        
        from sklearn.metrics.pairwise import cosine_similarity
        print("✓ Scikit-learn imported")
        
        from transformers import pipeline
        print("✓ Transformers imported")
        
        from supabase import create_client
        print("✓ Supabase imported")
        
        print("All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_model_loading():
    """Test if models can be loaded"""
    try:
        print("\nTesting model loading...")
        
        # Test sentence transformer
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        print("✓ SentenceTransformer model loaded")
        
        # Test transformers pipeline
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        print("✓ BART summarization model loaded")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without API"""
    try:
        print("\nTesting basic functionality...")
        
        # Add backend to path
        backend_dir = os.path.join(os.path.dirname(__file__), 'app')
        sys.path.insert(0, backend_dir)
        
        # Test embedding
        from embed_utils import chunk_text, embed_chunks, search_chunks
        
        text = "This is a test document. It has multiple sentences. We will test chunking and embedding."
        chunks = chunk_text(text)
        print(f"✓ Text chunked into {len(chunks)} chunks")
        
        if chunks:
            embeddings = embed_chunks(chunks)
            print(f"✓ Embeddings created with shape {embeddings.shape}")
            
            results = search_chunks("test document", chunks, embeddings, top_k=2)
            print(f"✓ Search returned {len(results)} results")
        
        # Test PDF utils (without actual PDF)
        from pdf_utils import extract_text_from_pdf
        print("✓ PDF utilities imported")
        
        # Test summarizer
        from summarizer_utils import summarize_text
        short_text = "This is a short text that needs to be summarized for testing purposes."
        summary = summarize_text(short_text)
        print(f"✓ Summarization working: {len(summary)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("PaperMind AI - System Test")
    print("=" * 40)
    
    all_tests_passed = True
    
    all_tests_passed &= test_imports()
    all_tests_passed &= test_model_loading()
    all_tests_passed &= test_basic_functionality()
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✅ All tests passed! PaperMind AI is functional.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
