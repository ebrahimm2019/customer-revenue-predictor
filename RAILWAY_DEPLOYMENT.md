# 🚂 RAILWAY DEPLOYMENT GUIDE

## Problem You're Facing

Railway can't see your Python files - only README.md. This means the project wasn't properly pushed to GitHub.

---

## ✅ SOLUTION - Complete Step-by-Step

### STEP 1: Prepare Your Project for Git

```bash
# Navigate to project
cd customer-revenue-predictor

# Initialize Git
git init

# Create proper .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
*.egg-info/
.venv/
venv/
ENV/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment
.env

# Large files - DON'T commit these
Year 2009-2010.csv
Year 2010-2011.csv
models/trained_model.pkl

# Keep directory structure
!models/.gitkeep
!data/.gitkeep
EOF

# Create directory placeholders
mkdir -p models data
touch models/.gitkeep data/.gitkeep

# Add all files
git add .

# Commit
git commit -m "Initial commit: Customer Revenue Predictor"
```

---

### STEP 2: Push to GitHub

**A. Create Repository on GitHub:**
1. Go to https://github.com/new
2. Repository name: `customer-revenue-predictor`
3. Make it **Public** or **Private**
4. **DON'T** initialize with README (you already have one)
5. Click "Create repository"

**B. Push Your Code:**
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/customer-revenue-predictor.git

git branch -M main

git push -u origin main
```

**Verify:** Go to your GitHub repo URL - you should see all your files.

---

### STEP 3: Deploy on Railway

**A. Connect Railway to GitHub:**

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select `customer-revenue-predictor` repo
6. Click **"Deploy Now"**

**B. Railway Auto-Detection:**

Railway will:
- ✅ Detect Python project
- ✅ Read `requirements.txt`
- ✅ Install dependencies
- ✅ Start server with Procfile or detect uvicorn
- ✅ Assign public URL

**Wait 2-5 minutes for build...**

---

### STEP 4: Handle the Model File Issue

Railway can't access your local trained model. **Choose one option:**

#### **Option A: Demo Mode (Quick Test)**

The app will run without predictions. Good for testing UI.

**In Railway Dashboard:**
- No changes needed
- App will start, but `/api/predict` won't work
- UI and other pages will load fine

#### **Option B: Train on Railway (Not Recommended)**

Issues:
- ❌ Dataset CSVs are too large for git
- ❌ Free tier has limited memory
- ❌ Training takes time on cold start

#### **Option C: Use Pre-trained Model URL (BEST)**

**Step 1:** Upload model to cloud storage
```bash
# Option 1: GitHub Release
# - Create new release on GitHub
# - Upload trained_model.pkl as asset
# - Copy download URL

# Option 2: Google Drive
# - Upload trained_model.pkl
# - Set to "Anyone with link can view"
# - Get direct download link

# Option 3: Dropbox
# - Upload file
# - Get sharing link
# - Change ?dl=0 to ?dl=1 for direct download
```

**Step 2:** Update code to download model

Create `app/ml/model_loader.py`:
```python
import os
import pickle
import urllib.request
from pathlib import Path

def load_model_from_url(model_path: Path):
    """Download model from URL if not exists."""
    model_url = os.getenv("MODEL_URL")
    
    if model_url and not model_path.exists():
        print(f"📥 Downloading model from {model_url}")
        model_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(model_url, model_path)
        print(f"✅ Model downloaded to {model_path}")
    
    with open(model_path, 'rb') as f:
        return pickle.load(f)
```

**Step 3:** Set environment variable in Railway
- Railway Dashboard → Your Project → Variables
- Add: `MODEL_URL` = `https://your-model-url.com/trained_model.pkl`
- Redeploy

---

### STEP 5: Verify Deployment

After build completes:

**A. Check Railway Logs:**
```
✓ Build successful
✓ Starting server
✓ Model loaded (if using MODEL_URL)
```

**B. Test Endpoints:**
```bash
# Replace with your Railway URL
export RAILWAY_URL="https://your-app.railway.app"

# Health check
curl $RAILWAY_URL/api/health

# Open in browser
open $RAILWAY_URL
```

**C. Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

## 🔧 Troubleshooting Railway Build

### Issue: "No buildpack found"
**Solution:** Ensure `requirements.txt` exists in root:
```bash
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### Issue: "Build failed - memory limit"
**Solution:** 
1. Railway free tier: 512MB RAM
2. Reduce model size or upgrade tier
3. Use model URL approach

### Issue: "Module not found"
**Solution:** Check `requirements.txt` has all dependencies:
```bash
# Regenerate from uv
uv pip compile pyproject.toml > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue: "Port binding error"
**Solution:** Ensure using `$PORT` environment variable:
```python
# In run.py or uvicorn command
port = int(os.getenv("PORT", 8000))
```

---

## 📋 Railway Configuration Files

These files help Railway understand your app:

### **requirements.txt** (Required)
```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pandas>=2.2.0
numpy>=1.26.0
scikit-learn>=1.5.0
xgboost>=2.1.0
pydantic>=2.9.0
python-multipart>=0.0.9
```

### **Procfile** (Optional - helps Railway)
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **nixpacks.toml** (Optional - fine-tune build)
```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### **railway.json** (Optional - deployment config)
```json
{
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
  }
}
```

---

## 🎯 Recommended Deployment Strategy

### For Testing/Demo:
```bash
1. Push to GitHub (without model/datasets)
2. Deploy on Railway
3. App runs in "demo mode" - UI works, predictions disabled
4. Show stakeholders the interface
```

### For Production:
```bash
1. Train model locally
2. Upload to cloud storage (GitHub Release/GCS/S3)
3. Add MODEL_URL to Railway environment
4. Code auto-downloads model on startup
5. Full functionality available
```

---

## 💰 Railway Free Tier Limits

- **Execution:** 500 hours/month
- **Memory:** 512MB RAM
- **Storage:** 1GB
- **Bandwidth:** Unlimited

**Enough for:**
- ✅ Demo/testing
- ✅ Portfolio projects
- ✅ Small user base

**Not enough for:**
- ❌ Training large models
- ❌ High-traffic production
- ❌ Storing large datasets

---

## 🚀 Alternative: Deploy with Railway CLI

If GitHub is giving you trouble:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project (from your local directory)
cd customer-revenue-predictor
railway link

# Deploy directly
railway up

# Set environment variables
railway variables set MODEL_URL=https://your-url.com/model.pkl

# Check logs
railway logs
```

---

## ✅ Success Checklist

Before deploying:
- [ ] All code committed to git
- [ ] `.gitignore` excludes large files
- [ ] `requirements.txt` in root
- [ ] Pushed to GitHub
- [ ] Can see all files on GitHub (except ignored ones)
- [ ] Railway connected to GitHub repo
- [ ] Environment variables set (if needed)

After deploying:
- [ ] Build successful in Railway logs
- [ ] `/api/health` returns healthy status
- [ ] Can open landing page
- [ ] (Optional) Predictions work if model loaded

---

## 📞 Need Help?

1. **Check Railway logs:**
   - Railway Dashboard → Deployments → View Logs

2. **Common fixes:**
   - Clear build cache (Railway Dashboard → Settings)
   - Redeploy (Railway Dashboard → Deployments → Redeploy)
   - Check environment variables

3. **Still stuck?**
   - Railway has excellent Discord support
   - Check: https://docs.railway.app

---

## 🎉 You're Live!

Once deployed successfully:

```
🌐 Your app URL: https://customer-revenue-predictor.railway.app

📊 Pages:
- Landing: /
- Dashboard: /dashboard
- Predict: /predict
- Insights: /insights

🔌 API Docs: /docs
```

**Share your Railway URL with stakeholders!** 🚀
