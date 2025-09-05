# Railway Deployment Guide for PaperMind AI

## Quick Deploy to Railway (Recommended)

### 1. Setup Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub repository

### 2. Deploy Backend
```bash
# Create railway.json in project root
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python start_production.py",
    "healthcheckPath": "/health"
  }
}
```

### 3. Environment Variables
Set these in Railway dashboard:
- `ENVIRONMENT=production`
- `PYTHON_VERSION=3.11.9`
- `SUPABASE_URL=your_supabase_url`
- `SUPABASE_KEY=your_supabase_key`

### 4. Deploy Frontend
Create separate service for frontend:
- Build Command: `cd frontend && npm install`
- Start Command: `cd frontend && npm start`

## Alternative: Google Cloud Run

### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
CMD ["python", "start_production.py"]
```

### 2. Deploy
```bash
gcloud run deploy papermind-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 2Gi
```

## Railway Advantages:
- ✅ 8GB RAM (vs 512MB on Render)
- ✅ $5 free credit monthly
- ✅ Automatic GitHub deployments
- ✅ Better for AI/ML apps
- ✅ Global edge deployment
- ✅ PostgreSQL database included

## Quick Railway Setup:
1. Push your code to GitHub
2. Connect Railway to your repo
3. Deploy automatically
4. Set environment variables
5. Your app is live!

Railway URL format: `https://your-app.railway.app`
