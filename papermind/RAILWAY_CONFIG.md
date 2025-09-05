# Railway Configuration for PaperMind AI

## Backend Service
- **Start Command**: `cd backend && python start_production.py`
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Health Check**: `/health`
- **Port**: Auto-detected from $PORT environment variable

## Environment Variables to Set:
```
ENVIRONMENT=production
PYTHON_VERSION=3.11.9
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

## Memory Allocation:
- **Default**: 8GB RAM (more than enough for all AI models)
- **CPU**: 8 vCPU cores
- **Cost**: $5 free credit monthly

## Domain:
- **Auto-generated**: `https://papermind-ai-backend-production.up.railway.app`
- **Custom domain**: Available on paid plans

## Database:
- Railway provides PostgreSQL if needed
- Currently using Supabase (external)

## Deployment Steps:
1. Connect GitHub repository
2. Deploy backend service first
3. Set environment variables
4. Deploy frontend as separate service
5. Update frontend API URL to point to Railway backend

## File Structure Optimized for Railway:
```
papermind/
├── Procfile              # Railway start command
├── railway.json          # Railway configuration
├── backend/
│   ├── requirements.txt  # Python dependencies
│   ├── start_production.py
│   └── app/
└── frontend/
    ├── package.json      # Node.js dependencies
    └── index.html
```
