"""Pydantic models for API."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CustomerFeatures(BaseModel):
    """Customer features for prediction."""
    customer_id: Optional[str] = None
    frequency: int = Field(..., ge=0)
    monetary_total: float = Field(..., ge=0)
    recency: int = Field(..., ge=0)
    n_purchase_days: Optional[int] = 0
    n_orders_items: Optional[int] = 0
    tenure_days: Optional[int] = 1
    customer_age: Optional[int] = 1
    rev_30d: Optional[float] = 0.0
    rev_90d: Optional[float] = 0.0
    rev_180d: Optional[float] = 0.0
    rev_365d: Optional[float] = 0.0
    rev_prev_90d: Optional[float] = 0.0
    is_uk: Optional[bool] = True


class PredictionResponse(BaseModel):
    """Prediction response."""
    predicted_revenue: float
    confidence_interval: Dict[str, float]
    segment: str
    segment_color: str
    segment_description: str
    recommended_action: str
    risk_level: str
    insights: List[str]


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    customers: List[CustomerFeatures]


class ModelInfoResponse(BaseModel):
    """Model info."""
    model_type: str
    n_features: int
    training_metrics: Optional[Dict[str, float]] = None


class HealthResponse(BaseModel):
    """Health check."""
    status: str
    model_loaded: bool
    version: str
