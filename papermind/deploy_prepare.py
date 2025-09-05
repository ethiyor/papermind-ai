#!/usr/bin/env python3
"""
PaperMind AI - Quick Deployment Script
Helps prepare the project for Render deployment
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_requirements():
    """Check if all required files exist"""
    print("📋 Checking deployment requirements...")
    
    required_files = [
        "render.yaml",
        ".renderignore", 
        "backend/requirements.txt",
        "backend/runtime.txt",
        "backend/app/main.py",
        "frontend/index.html",
        "frontend/style.css"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def update_git():
    """Add and commit all changes"""
    print("📤 Preparing Git repository...")
    
    commands = [
        ("git add .", "Adding all files to git"),
        ("git status", "Checking git status"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    # Check if there are changes to commit
    result = subprocess.run("git diff --cached --exit-code", shell=True, capture_output=True)
    if result.returncode != 0:  # There are changes
        commit_message = "Prepare for Render deployment - Add deployment configs and optimize for production"
        if run_command(f'git commit -m "{commit_message}"', "Committing changes"):
            print("✅ Changes committed successfully")
        else:
            return False
    else:
        print("ℹ️  No changes to commit")
    
    return True

def main():
    """Main deployment preparation function"""
    print("🚀 PaperMind AI - Render Deployment Preparation")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Deployment preparation failed!")
        print("Please ensure all required files are present.")
        sys.exit(1)
    
    # Update git repository
    if not update_git():
        print("\n❌ Git preparation failed!")
        sys.exit(1)
    
    print("\n🎉 Deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Push to GitHub: git push origin main")
    print("2. Go to render.com and create a new account")
    print("3. Connect your GitHub repository")
    print("4. Follow the deployment guide in RENDER_DEPLOYMENT_GUIDE.md")
    print("5. Use the checklist in DEPLOYMENT_CHECKLIST.md")
    
    print("\n🔗 Quick Links:")
    print("- Render: https://render.com")
    print("- Deployment Guide: ./RENDER_DEPLOYMENT_GUIDE.md")
    print("- Deployment Checklist: ./DEPLOYMENT_CHECKLIST.md")
    
    print("\n💡 Pro Tips:")
    print("- Use render.yaml for automatic deployment")
    print("- Set environment variables in Render dashboard")
    print("- Monitor your app in Render dashboard")
    print("- Update frontend URLs after backend deployment")

if __name__ == "__main__":
    main()
