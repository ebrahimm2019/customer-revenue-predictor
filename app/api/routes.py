"""API routes."""
from fastapi import APIRouter, HTTPException, UploadFile, File
import pandas as pd
import io

from .models import (CustomerFeatures, PredictionResponse, BatchPredictionRequest,
                     ModelInfoResponse, HealthResponse)
from ..ml.predictor import get_prediction_service
from ..config import settings

router = APIRouter()


@router.post("/predict/single", response_model=PredictionResponse)
async def predict_single(customer: CustomerFeatures):
    """Predict single customer revenue."""
    try:
        service = get_prediction_service()
        result = service.predict_single(customer.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Predict batch of customers."""
    try:
        service = get_prediction_service()
        customers_data = [c.model_dump() for c in request.customers]
        predictions = service.predict_batch(customers_data)
        
        successful = [p for p in predictions if p.get('success', False)]
        total_predicted = sum(p['predicted_revenue'] for p in successful)
        
        return {
            "predictions": predictions,
            "summary": {
                "total": len(predictions),
                "successful": len(successful),
                "total_predicted_revenue": round(total_predicted, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    """Get model information."""
    try:
        service = get_prediction_service()
        return service.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model/features")
async def feature_importance():
    """Get feature importance."""
    try:
        service = get_prediction_service()
        return {"features": service.get_feature_importance(top_n=10)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check."""
    try:
        service = get_prediction_service()
        model_loaded = service.model is not None
        return {
            "status": "healthy" if model_loaded else "degraded",
            "model_loaded": model_loaded,
            "version": settings.API_VERSION
        }
    except:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "version": settings.API_VERSION
        }
