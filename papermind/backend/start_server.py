#!/usr/bin/env python3
"""
Standalone server script for PaperMind AI
"""
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import after path setup
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting PaperMind AI server...")
    print(f"Backend directory: {backend_dir}")
    print(f"Python path: {sys.path[:3]}...")
    
    # Start the server
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        access_log=True
    )
