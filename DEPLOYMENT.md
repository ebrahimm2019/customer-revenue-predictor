# 🚀 DEPLOYMENT GUIDE - Customer Revenue Predictor

## Quick Deploy Options

### ⭐ Option 1: Railway.app (RECOMMENDED - Easiest)

**Why Railway:** Zero-config, free 500hrs/month, auto-detects Python, instant deployment

**Steps:**

1. **Prepare Repository**
   ```bash
   cd customer-revenue-predictor
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub**
   ```bash
   # Create repo on GitHub first
   git remote add origin https://github.com/YOUR_USERNAME/customer-revenue-predictor.git
   git push -u origin main
   ```

3. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Python and builds
   - Get instant URL: `https://your-app.railway.app`

4. **Environment Variables (Optional)**
   - In Railway dashboard, add:
     ```
     PORT=8000
     PYTHON_VERSION=3.11
     ```

5. **Test**
   ```bash
   curl https://your-app.railway.app/api/health
   ```

**That's it!** Railway handles everything automatically.

---

### Option 2: Render.com (Most Reliable)

**Why Render:** More generous free tier, built-in PostgreSQL, auto-sleep

**Steps:**

1. **Sign up at render.com**

2. **Create Web Service**
   - Dashboard → New → Web Service
   - Connect GitHub repo

3. **Configure**
   - Name: `customer-revenue-predictor`
   - Build Command: `pip install uv && uv sync`
   - Start Command: `uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: Free

4. **Deploy**
   - Render builds and deploys (takes 5-10 mins first time)
   - Get URL: `https://customer-revenue-predictor.onrender.com`

**Note:** Free tier sleeps after 15 mins inactivity. First request after sleep takes ~30s to wake up.

---

### Option 3: Fly.io (Best Performance)

**Why Fly:** Fast global CDN, no cold starts, generous free tier

**Steps:**

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Launch (from project root)**
   ```bash
   fly launch
   # Answer prompts:
   # - App name: customer-revenue-predictor
   # - Region: choose closest to you
   # - Deploy: yes
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

5. **Open**
   ```bash
   fly open
   ```

**Free Tier:** 3 shared-CPU VMs with 256MB RAM each

---

### Option 4: Docker (Any Cloud)

**Universal deployment for AWS, GCP, Azure, DigitalOcean, etc.**

1. **Build Image**
   ```bash
   docker build -t customer-revenue-predictor .
   ```

2. **Run Locally**
   ```bash
   docker run -p 8000:8000 customer-revenue-predictor
   ```

3. **Deploy to Cloud**
   
   **AWS ECS:**
   ```bash
   # Push to ECR
   aws ecr create-repository --repository-name customer-revenue-predictor
   docker tag customer-revenue-predictor:latest AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/customer-revenue-predictor
   docker push AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/customer-revenue-predictor
   
   # Create ECS service (via console or CLI)
   ```

   **Google Cloud Run:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/customer-revenue-predictor
   gcloud run deploy --image gcr.io/PROJECT_ID/customer-revenue-predictor --platform managed
   ```

   **Azure Container Instances:**
   ```bash
   az container create --resource-group mygroup --name customer-revenue-predictor \
     --image your-registry.azurecr.io/customer-revenue-predictor \
     --dns-name-label customer-revenue-predictor --ports 8000
   ```

---

## 🔧 Pre-Deployment Checklist

Before deploying, make sure you have:

- [x] Trained the model (`uv run python scripts/train_model.py`)
- [x] Model file exists: `models/trained_model.pkl`
- [x] Tested locally (`uv run uvicorn app.main:app --reload`)
- [x] All dependencies in `pyproject.toml` or `requirements.txt`
- [x] Dataset CSVs in project root (for training)

---

## 🧪 Testing Deployment

After deployment, test all endpoints:

```bash
# Replace URL with your deployment URL
export API_URL="https://your-app.railway.app"

# 1. Health check
curl $API_URL/api/health

# 2. Model info
curl $API_URL/api/model/info

# 3. Predict single customer
curl -X POST $API_URL/api/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "test123",
    "frequency": 10,
    "monetary_total": 3500.0,
    "recency": 30,
    "rev_90d": 1200.0,
    "is_uk": true
  }'

# 4. Feature importance
curl $API_URL/api/model/features
```

---

## 🔐 Security for Production

If moving to production:

1. **Add Authentication**
   ```python
   # In app/main.py
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   @router.post("/predict/single")
   async def predict(customer: CustomerFeatures, credentials: HTTPAuthorizationCredentials = Depends(security)):
       # Verify token
       pass
   ```

2. **Rate Limiting**
   ```bash
   pip install slowapi
   ```
   
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

3. **HTTPS Only** (auto on Railway/Render/Fly)

4. **Environment Variables**
   - Never commit `models/` to public repos
   - Use S3/GCS for model storage
   - Load from environment:
     ```python
     MODEL_URL = os.getenv("MODEL_URL")
     ```

---

## 📊 Monitoring

**Railway:** Built-in metrics dashboard
**Render:** Logs in dashboard
**Fly:** `fly logs` command

**Add Application Monitoring:**
```bash
# Sentry for error tracking
pip install sentry-sdk[fastapi]
```

```python
import sentry_sdk
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"))
```

---

## 💰 Cost Estimates

| Platform | Free Tier | Paid (if needed) |
|----------|-----------|------------------|
| **Railway** | 500 hrs/month | $5/month for 500 more hrs |
| **Render** | 750 hrs/month | $7/month for always-on |
| **Fly.io** | 3 VMs, 256MB | $1.94/month per additional VM |
| **Vercel** | Not ideal for ML (serverless limits) | N/A |
| **Heroku** | No longer free | $7/month minimum |

**Recommendation:** Start with Railway free tier. Upgrade when you hit limits.

---

## 🐛 Troubleshooting

### Issue: "Model file not found"
```bash
# Train model first
uv run python scripts/train_model.py
```

### Issue: "Module not found"
```bash
# Reinstall dependencies
uv sync
```

### Issue: "Port already in use"
```bash
# Change port
uv run uvicorn app.main:app --port 8001
```

### Issue: "Dataset not found"
- Ensure `Year 2009-2010.csv` and `Year 2010-2011.csv` are in project root
- Check file names match exactly (case-sensitive)

### Issue: Railway/Render build fails
- Check build logs in dashboard
- Ensure `requirements.txt` exists
- Verify Python version (3.9+)

---

## 🔄 CI/CD Setup (Optional)

**GitHub Actions for auto-deploy:**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      - name: Deploy
        run: railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## ✅ Post-Deployment

After successful deployment:

1. **Update README** with live demo URL
2. **Test all pages**
   - Landing: `/`
   - Dashboard: `/dashboard`
   - Predict: `/predict`
   - Insights: `/insights`
   - API: `/api/health`

3. **Monitor logs** for first 24 hours
4. **Share with stakeholders**
5. **Gather feedback**

---

## 🎉 You're Live!

Your Customer Revenue Predictor is now deployed and accessible worldwide!

**Next Steps:**
- Integrate with CRM via API
- Set up scheduled batch predictions
- Add more features based on feedback
- Scale as needed

**Need help?** Check Railway/Render docs or reach out to their support (excellent on all platforms).
