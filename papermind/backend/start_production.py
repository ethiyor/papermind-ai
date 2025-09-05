#!/usr/bin/env python3
"""
Production server startup script for PaperMind AI
Optimized for Render deployment
"""
import os
import sys
import uvicorn
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    """Start the production server"""
    # Get port from environment (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Set environment variables for production
    os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Avoid tokenizer warnings
    
    print(f"🚀 Starting PaperMind AI server on port {port}")
    print(f"📍 Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    print(f"🔧 Python version: {sys.version}")
    
    # Configure uvicorn for production
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": port,
        "workers": 1,  # Single worker for free tier
        "timeout_keep_alive": 30,
        "timeout_graceful_shutdown": 10,
        "max_requests": 1000,
        "max_requests_jitter": 50,
    }
    
    # Add production-specific settings
    if os.environ.get("ENVIRONMENT") == "production":
        config.update({
            "access_log": True,
            "use_colors": False,
            "log_level": "info",
        })
    else:
        config.update({
            "reload": True,
            "log_level": "debug",
        })
    
    # Start the server
    uvicorn.run(**config)

if __name__ == "__main__":
    main()
