# Customer Revenue Predictor

**Production-ready AI system for predicting customer future revenue using advanced machine learning.**

Built with FastAPI, XGBoost, and modern web technologies. Transforms notebook ML experiments into a professional client-facing product.

---

## 🎯 What This System Does

Predicts **future customer revenue** based on purchase history using:
- 30 engineered features (RFM, temporal patterns, lifecycle, basket behavior)
- XGBoost regression model (R² = 0.9935, RMSE = £259)
- Intelligent customer segmentation (VIP / High Value / Growth / At Risk)
- Confidence intervals and actionable business insights

**Perfect for:**
- Marketing teams targeting high-value customers
- Customer success teams preventing churn
- Finance teams forecasting revenue
- Business analysts understanding customer behavior

---

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| **R² Score** | 0.9935 (99.35% variance explained) |
| **RMSE** | £259 |
| **MAE** | £170 |
| **Dataset** | 1M+ transactions, 4,249 customers |
| **Features** | 30 engineered predictors |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- [UV](https://github.com/astral-sh/uv) (modern Python package manager)
- Online Retail II dataset from UCI

### Installation

```bash
# 1. Clone/download the project
cd customer-revenue-predictor

# 2. Install dependencies with UV
uv sync

# 3. Place dataset CSVs in project root
# Required files:
#   - Year 2009-2010.csv
#   - Year 2010-2011.csv

# 4. Train the model
uv run python scripts/train_model.py

# 5. Start the API server
uv run uvicorn app.main:app --reload
```

Navigate to **http://localhost:8000** 🎉

---

## 📁 Project Structure

```
customer-revenue-predictor/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration
│   ├── api/                 # API layer
│   │   ├── routes.py        # Endpoints
│   │   └── models.py        # Pydantic schemas
│   ├── ml/                  # ML core
│   │   ├── predictor.py     # Prediction service
│   │   ├── features.py      # Feature engineering
│   │   └── segmentation.py  # Customer segmentation
│   └── static/              # Frontend (HTML/CSS/JS)
├── models/                  # Trained models
│   ├── trained_model.pkl
│   └── model_metadata.json
├── data/
│   └── sample_customers.csv # Example input
├── scripts/
│   └── train_model.py       # Model training
├── deployment/              # Deployment configs
└── pyproject.toml           # UV dependencies
```

---

## 🔌 API Endpoints

### POST `/api/predict/single`
Predict revenue for single customer

```bash
curl -X POST http://localhost:8000/api/predict/single \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "12345",
    "frequency": 8,
    "monetary_total": 2500.0,
    "recency": 45,
    "rev_90d": 800.0,
    "is_uk": true
  }'
```

**Response:**
```json
{
  "predicted_revenue": 1245.67,
  "confidence_interval": {"lower": 1075.67, "upper": 1415.67},
  "segment": "Growth",
  "segment_color": "#3B82F6",
  "risk_level": "Low",
  "insights": [
    "✓ Active: Last purchase 45 days ago",
    "📈 Growing: +£200 recent revenue"
  ]
}
```

### POST `/api/predict/batch`
Predict for multiple customers (up to 1000)

### GET `/api/model/info`
Get model metadata and training metrics

### GET `/api/model/features`
Get feature importance

### GET `/api/health`
Health check

---

## 🎨 Web Interface

### **Dashboard** (`/dashboard`)
- Customer base overview
- Segment distribution
- Revenue forecasts
- KPI cards

### **Prediction** (`/predict`)
- Single customer prediction form
- Batch CSV upload
- Real-time results

### **Insights** (`/insights`)
- Feature importance charts
- Model performance metrics
- Business interpretation

---

## 🧠 Feature Engineering

The system uses 30 features across 6 categories:

| Category | Features | Business Meaning |
|----------|----------|------------------|
| **RFM Core** | frequency, monetary_total, recency, AOV | Basic purchase patterns |
| **Temporal Windows** | rev_30d, rev_90d, rev_180d, rev_365d | Recent activity tracking |
| **Revenue Trends** | revenue_growth_rate, revenue_trend_ratio | Momentum indicators |
| **Lifecycle** | freq_rate, maturity, recent_ratio | Customer engagement |
| **Basket Behavior** | avg_basket_rev, order_cv, n_orders | Purchase characteristics |
| **Behavioral** | q4_frac, weekend_ratio, is_uk | Seasonality & geography |

---

## 🚢 Deployment

### Option 1: Railway.app (Recommended - Easiest)

**Why Railway:**
- ✅ Free tier (500 hours/month)
- ✅ Zero config deployment
- ✅ Auto-detects Python + builds
- ✅ Free PostgreSQL if needed
- ✅ Custom domains

**Steps:**

1. **Sign up at [railway.app](https://railway.app)**

2. **Create new project → Deploy from GitHub**
   - Connect your repo
   - Railway auto-detects Python project

3. **Add environment variables (optional):**
   ```
   PORT=8000
   ```

4. **Deploy!**
   - Railway builds and deploys automatically
   - Get public URL: `your-app.railway.app`

**Commands (optional):**
```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login
railway login

# Deploy from terminal
railway up
```

---

### Option 2: Render.com (Most Reliable)

**Why Render:**
- ✅ Free tier (750 hours/month)
- ✅ Auto-sleep after inactivity
- ✅ Built-in PostgreSQL
- ✅ Easy custom domains

**Steps:**

1. **Sign up at [render.com](https://render.com)**

2. **Create Web Service**
   - New → Web Service
   - Connect GitHub repo

3. **Configure:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Deploy!**

**Note:** Create `requirements.txt` first:
```bash
uv pip compile pyproject.toml > requirements.txt
```

---

### Option 3: Fly.io (Best Performance)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch (from project root)
fly launch

# Deploy
fly deploy
```

---

### Option 4: Docker (Any Platform)

```dockerfile
# Dockerfile (create in project root)
FROM python:3.11-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy project
COPY . .

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 8000

# Run
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t customer-revenue-predictor .
docker run -p 8000:8000 customer-revenue-predictor
```

---

## 🔧 Configuration

Edit `app/config.py` to customize:

```python
# Segment thresholds
SEGMENT_THRESHOLDS = {
    "vip": 10000,        # £10K+ predicted
    "high_value": 2000,  # £2K-£10K
    "growth": 500,       # £500-£2K
    "at_risk": 0,        # < £500
}

# CORS origins
CORS_ORIGINS = [
    "http://localhost:8000",
    "https://yourdomain.com"
]
```

---

## 📦 Deployment Files Included

| File | Purpose |
|------|---------|
| `railway.json` | Railway auto-config |
| `render.yaml` | Render blueprint |
| `fly.toml` | Fly.io configuration |
| `Dockerfile` | Container build |

---

## 🧪 Testing

```bash
# Run model training
uv run python scripts/train_model.py

# Start server
uv run uvicorn app.main:app --reload

# Test prediction
curl -X POST http://localhost:8000/api/predict/single \
  -H "Content-Type: application/json" \
  -d @data/sample_customers.json

# Health check
curl http://localhost:8000/api/health
```

---

## 📝 Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-model

# 2. Make changes, retrain model
uv run python scripts/train_model.py

# 3. Test locally
uv run uvicorn app.main:app --reload

# 4. Deploy
git push origin feature/new-model
# Deployment platforms auto-build from GitHub
```

---

## 🎓 Model Training Details

The model replicates the notebook's best performer:

- **Algorithm:** XGBoost Regressor
- **Hyperparameters:**
  - n_estimators: 300
  - max_depth: 6
  - learning_rate: 0.05
  - subsample: 0.8
  - colsample_bytree: 0.8
- **Temporal Split:** Oct 1, 2011
- **Training:** Calibration period (2009-2011)
- **Validation:** Holdout period (Oct-Dec 2011)

---

## 🚨 Troubleshooting

### Model file not found
```bash
# Train the model first
uv run python scripts/train_model.py
```

### Dataset missing
- Download UCI Online Retail II dataset
- Place `Year 2009-2010.csv` and `Year 2010-2011.csv` in project root

### Port already in use
```bash
# Change port
uv run uvicorn app.main:app --port 8001
```

### UV not found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 🔮 Future Enhancements

**Model Improvements:**
- Three-stage XGBoost for better zero-inflation handling
- Quantile regression for better confidence intervals
- Ensemble of multiple models

**Features:**
- Customer lifetime value (CLV) prediction
- Churn probability scoring
- Segment transitions over time
- A/B testing framework

**Infrastructure:**
- Redis caching for predictions
- PostgreSQL for prediction history
- Celery for async batch jobs
- Monitoring with Prometheus

---

## 📄 License

MIT License - See LICENSE file

---

## 👨‍💻 Author

**Mohamed** - Senior AI/ML Engineer

Built for production deployment with focus on:
- Clean architecture
- Professional UX
- Business-friendly communication
- Easy maintenance

---

## 🙏 Acknowledgments

- **Dataset:** UCI Machine Learning Repository - Online Retail II
- **Framework:** FastAPI, XGBoost, scikit-learn
- **Deployment:** Railway, Render, Fly.io free tiers

---

**Ready to deploy?** Start with Railway for the easiest setup, or Render for maximum reliability. Both offer generous free tiers perfect for demos and MVPs.

For production at scale, consider upgrading to paid tiers or using Docker on AWS/GCP/Azure.
