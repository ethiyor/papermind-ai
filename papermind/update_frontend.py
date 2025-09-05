#!/usr/bin/env python3
"""
Update frontend configuration for production deployment
"""
import re
import sys
from pathlib import Path

def update_frontend_config(backend_url):
    """Update the frontend to use production backend URL"""
    
    frontend_dir = Path(__file__).parent / "frontend"
    index_file = frontend_dir / "index.html"
    
    if not index_file.exists():
        print(f"❌ Frontend file not found: {index_file}")
        return False
    
    # Read the current file
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace localhost URLs with production URL
    patterns_to_replace = [
        (r'http://127\.0\.0\.1:8000', backend_url),
        (r'http://localhost:8000', backend_url),
        (r'https?://.*\.onrender\.com', backend_url),  # Replace any existing Render URL
    ]
    
    original_content = content
    
    for pattern, replacement in patterns_to_replace:
        content = re.sub(pattern, replacement, content)
    
    # Check if any changes were made
    if content == original_content:
        print(f"⚠️  No API URLs found to update in {index_file}")
        return False
    
    # Write the updated content
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated frontend API URLs to: {backend_url}")
    return True

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python update_frontend.py <backend_url>")
        print("Example: python update_frontend.py https://papermind-ai-backend.onrender.com")
        sys.exit(1)
    
    backend_url = sys.argv[1].rstrip('/')  # Remove trailing slash
    
    # Validate URL format
    if not backend_url.startswith(('http://', 'https://')):
        print("❌ Backend URL must start with http:// or https://")
        sys.exit(1)
    
    print(f"🔧 Updating frontend configuration...")
    print(f"📍 Backend URL: {backend_url}")
    
    success = update_frontend_config(backend_url)
    
    if success:
        print("🎉 Frontend configuration updated successfully!")
        print("💡 Commit and push the changes to deploy the updated frontend")
    else:
        print("❌ Failed to update frontend configuration")
        sys.exit(1)

if __name__ == "__main__":
    main()
