"""
Configuration management for the Customer Revenue Predictor application.
"""
import os
from pathlib import Path
from typing import Optional

class Settings:
    """Application settings and configuration."""
    
    # Project paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    DATA_DIR: Path = BASE_DIR / "data"
    STATIC_DIR: Path = BASE_DIR / "app" / "static"
    
    # Model files
    MODEL_PATH: Path = MODELS_DIR / "trained_model.pkl"
    FEATURE_CONFIG_PATH: Path = MODELS_DIR / "feature_config.json"
    MODEL_METADATA_PATH: Path = MODELS_DIR / "model_metadata.json"
    
    # API settings
    API_TITLE: str = "Customer Revenue Predictor API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Predict future customer revenue using advanced ML techniques"
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://*.railway.app",
        "https://*.render.com",
        "https://*.fly.dev",
    ]
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Business rules
    SEGMENT_THRESHOLDS = {
        "vip": 10000,        # £10K+ predicted revenue
        "high_value": 2000,  # £2K+ predicted revenue
        "growth": 500,       # £500+ predicted revenue
        "at_risk": 0,        # Everything else
    }
    
    # Feature definitions for UI
    FEATURE_DESCRIPTIONS = {
        "frequency": "Number of unique purchases",
        "monetary_total": "Total historical spending",
        "recency": "Days since last purchase",
        "tenure_days": "Days between first and last purchase",
        "customer_age": "Days since first purchase",
        "aov": "Average order value",
        "rev_30d": "Revenue in last 30 days",
        "rev_90d": "Revenue in last 90 days",
        "rev_180d": "Revenue in last 6 months",
        "rev_365d": "Revenue in last year",
        "revenue_growth_rate": "Recent revenue growth trend",
        "freq_rate": "Purchase frequency over lifetime",
        "maturity": "Customer engagement stability",
        "recent_ratio": "Recent vs total revenue ratio",
        "avg_basket_rev": "Average basket revenue",
        "n_orders": "Total number of orders",
        "q4_frac": "Fraction of revenue in Q4",
        "is_uk": "UK-based customer (1=yes, 0=no)",
    }

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.MODELS_DIR.mkdir(exist_ok=True, parents=True)
        cls.DATA_DIR.mkdir(exist_ok=True, parents=True)


# Global settings instance
settings = Settings()
settings.ensure_directories()
