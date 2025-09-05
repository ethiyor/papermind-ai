# Railway Manual Configuration

Since Railway is having issues with the cached build configuration, please manually set these in your Railway dashboard:

## Settings → Build & Deploy

### Build Command:
```
echo "Dependencies already installed in previous step"
```

### Start Command:
```
cd papermind/backend && python start_production.py
```

### Install Command (should auto-detect):
```
pip install -r papermind/requirements.txt
```

## Environment Variables
Make sure these are set in Variables tab:
- `ENVIRONMENT=production`
- `PYTHON_VERSION=3.11.9`

## Alternative: Create New Service
If the caching continues to cause issues:
1. Delete current service
2. Create new service from same GitHub repo
3. Let Railway auto-detect everything
4. Only override the Start Command to: `cd papermind/backend && python start_production.py`
