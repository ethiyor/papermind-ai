# PaperMind AI - Render Deployment Guide

## 🚀 Deploy PaperMind AI to Render

This guide will help you deploy your PaperMind AI application to Render, a modern cloud platform.

---

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Supabase Account** (Optional): For database storage

---

## 🔧 Step-by-Step Deployment

### **Step 1: Prepare Your Repository**

Make sure your repository has the following structure:
```
papermind/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── runtime.txt
│   └── start_server.py
├── frontend/
│   ├── index.html
│   └── style.css
├── render.yaml (created in this guide)
└── README.md
```

### **Step 2: Create Render Configuration**

We'll create a `render.yaml` file for automatic deployment configuration.

### **Step 3: Set Environment Variables**

In Render dashboard, you'll need to set:
- `PYTHON_VERSION=3.12.3`
- `SUPABASE_URL` (if using Supabase)
- `SUPABASE_KEY` (if using Supabase)

### **Step 4: Deploy Backend Service**

1. **Go to Render Dashboard**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `papermind-ai-backend` |
   | **Environment** | `Python 3` |
   | **Region** | Choose closest to your users |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### **Step 5: Deploy Frontend (Static Site)**

1. **Click "New +" → "Static Site"**
2. **Connect your GitHub repository**
3. **Configure:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `papermind-ai-frontend` |
   | **Branch** | `main` |
   | **Root Directory** | `frontend` |
   | **Build Command** | `echo "No build needed"` |
   | **Publish Directory** | `.` |

### **Step 6: Update Frontend API URLs**

After backend deployment, update the frontend to use your Render backend URL.

---

## 📁 Required Files

### **1. Update requirements.txt (if needed)**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pdfminer.six==20231228
sentence-transformers==2.2.2
scikit-learn==1.3.2
numpy==1.24.4
python-dotenv==1.0.0
pydantic==2.5.0
aiofiles==23.2.1
supabase==2.3.0
torch==2.1.1
transformers==4.36.0
tokenizers==0.15.0
```

### **2. Create Dockerfile (Optional)**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **3. Create .renderignore**
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
.venv
venv/
.git/
.pytest_cache/
test_models.py
complete_test.py
```

---

## 🔧 Configuration Updates Needed

### **Backend Updates for Production**

1. **CORS Configuration** - Update allowed origins
2. **Environment Variables** - Use Render's environment
3. **File Uploads** - Configure for cloud storage
4. **Database** - Use Supabase or PostgreSQL

### **Frontend Updates**

Update API URLs in your frontend JavaScript to point to your Render backend:

```javascript
// Change from:
const API_BASE = "http://127.0.0.1:8000";

// To:
const API_BASE = "https://your-backend-name.onrender.com";
```

---

## 🚀 Quick Deploy Commands

### **Option 1: Render YAML (Recommended)**

Create `render.yaml` and push to GitHub. Render will auto-deploy.

### **Option 2: Manual Deploy**

1. **Fork/Clone** your repository
2. **Push** to GitHub
3. **Connect** to Render
4. **Configure** as described above
5. **Deploy!**

---

## 🔍 Troubleshooting

### **Common Issues:**

1. **Build Fails**: Check Python version and requirements.txt
2. **App Won't Start**: Verify start command and port configuration
3. **CORS Errors**: Update CORS settings in FastAPI
4. **File Upload Issues**: Configure for cloud storage
5. **Model Loading**: May need to optimize for memory limits

### **Solutions:**

1. **Use specific package versions** in requirements.txt
2. **Set environment variables** correctly
3. **Update CORS origins** for your frontend domain
4. **Optimize model loading** for cloud deployment
5. **Use persistent storage** for uploaded files

---

## 📊 Monitoring & Scaling

### **Monitor Your App:**
- Use Render's built-in monitoring
- Check logs for errors
- Monitor resource usage

### **Scaling Options:**
- **Free Tier**: 750 hours/month
- **Starter**: $7/month
- **Standard**: $25/month

---

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit secrets
2. **HTTPS**: Render provides free SSL
3. **CORS**: Restrict to your frontend domain
4. **File Validation**: Validate uploads properly
5. **Rate Limiting**: Implement API rate limits

---

## 📝 Next Steps After Deployment

1. **Test all functionality** on the live site
2. **Set up monitoring** and alerts
3. **Configure custom domain** (optional)
4. **Set up backup strategy** for data
5. **Document API endpoints** for users

---

## 🎉 Success!

Once deployed, your PaperMind AI will be available at:
- **Backend**: `https://your-backend-name.onrender.com`
- **Frontend**: `https://your-frontend-name.onrender.com`

Your AI-powered PDF analysis tool is now live and ready for users worldwide! 🌍

---

**Need Help?** Check Render's documentation or the troubleshooting section above.
