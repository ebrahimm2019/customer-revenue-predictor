"""Main prediction service orchestrating model inference."""
import pickle
import json
from typing import Dict, Any, List
import numpy as np
import pandas as pd

from .features import FeatureEngineer
from .segmentation import CustomerSegmenter
from ..config import settings


class PredictionService:
    """Handles model loading and predictions."""
    
    def __init__(self):
        self.model = None
        self.feature_engineer = FeatureEngineer()
        self.model_metadata = {}
        self._load_model()
        self._load_metadata()
    
    def _load_model(self):
        """Load trained XGBoost model."""
        if not settings.MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {settings.MODEL_PATH}")
        
        with open(settings.MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✓ Model loaded: {settings.MODEL_PATH}")
    
    def _load_metadata(self):
        """Load model training metadata."""
        if settings.MODEL_METADATA_PATH.exists():
            with open(settings.MODEL_METADATA_PATH, 'r') as f:
                self.model_metadata = json.load(f)
            print(f"✓ Metadata loaded")
        else:
            print(f"⚠ No metadata file")
    
    def predict_single(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict revenue for single customer."""
        # Engineer features
        features = self.feature_engineer.engineer_from_dict(customer_data)
        self.feature_engineer.validate_features(features)
        
        # Predict
        predicted_revenue = float(self.model.predict(features)[0])
        predicted_revenue = max(0, predicted_revenue)
        
        # Segment
        segment, segment_meta = CustomerSegmenter.segment_customer(predicted_revenue)
        
        # Confidence interval (±MAE)
        mae = self.model_metadata.get('mae', 170)
        confidence_lower = max(0, predicted_revenue - mae)
        confidence_upper = predicted_revenue + mae
        
        # Risk assessment
        recency = customer_data.get('recency', 999)
        risk_level = CustomerSegmenter.get_risk_level(predicted_revenue, recency)
        
        # Insights
        insights = self._generate_insights(
            predicted_revenue, customer_data, segment, recency
        )
        
        return {
            "predicted_revenue": round(predicted_revenue, 2),
            "confidence_interval": {
                "lower": round(confidence_lower, 2),
                "upper": round(confidence_upper, 2)
            },
            "segment": segment,
            "segment_color": segment_meta["color"],
            "segment_description": segment_meta["description"],
            "recommended_action": segment_meta["action"],
            "risk_level": risk_level,
            "insights": insights
        }
    
    def predict_batch(self, customers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Predict for multiple customers."""
        results = []
        for customer_data in customers:
            try:
                result = self.predict_single(customer_data)
                result["customer_id"] = customer_data.get("customer_id", "unknown")
                result["success"] = True
                results.append(result)
            except Exception as e:
                results.append({
                    "customer_id": customer_data.get("customer_id", "unknown"),
                    "success": False,
                    "error": str(e)
                })
        return results
    
    def _generate_insights(self, predicted_revenue, customer_data, segment, recency):
        """Generate natural language insights."""
        insights = []
        
        if recency > 180:
            insights.append(f"⚠️ No purchase in {recency} days - consider re-engagement")
        elif recency < 30:
            insights.append(f"✓ Active: Last purchase {recency} days ago")
        
        trend = customer_data.get('rev_90d', 0) - customer_data.get('rev_prev_90d', 0)
        if trend > 500:
            insights.append(f"📈 Growing: +£{abs(trend):.0f} recent revenue")
        elif trend < -500:
            insights.append(f"📉 Declining: -£{abs(trend):.0f} recent revenue")
        
        aov = customer_data.get('aov', 0)
        if aov > 100:
            insights.append(f"💎 High AOV: £{aov:.0f} per order")
        
        frequency = customer_data.get('frequency', 0)
        if frequency > 20:
            insights.append(f"🔄 Frequent: {frequency} purchases")
        elif frequency < 3:
            insights.append(f"🆕 New: {frequency} purchase(s)")
        
        if segment == "VIP":
            insights.append("👑 VIP: Requires premium service")
        elif segment == "At Risk":
            insights.append("⚡ Action needed: Implement retention")
        
        return insights
    
    def get_feature_importance(self, top_n: int = 10) -> List[Dict]:
        """Get model feature importance."""
        if not hasattr(self.model, 'feature_importances_'):
            return []
        
        importance = self.model.feature_importances_
        features = self.feature_engineer.REQUIRED_FEATURES
        
        importance_list = [
            {
                "feature": feat,
                "importance": float(imp),
                "description": settings.FEATURE_DESCRIPTIONS.get(feat, "")
            }
            for feat, imp in zip(features, importance)
        ]
        
        importance_list.sort(key=lambda x: x['importance'], reverse=True)
        return importance_list[:top_n]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model metadata."""
        info = {
            "model_type": type(self.model).__name__,
            "n_features": self.feature_engineer.feature_count,
        }
        
        if self.model_metadata:
            info.update({
                "training_metrics": {
                    "rmse": self.model_metadata.get("rmse"),
                    "mae": self.model_metadata.get("mae"),
                    "r2": self.model_metadata.get("r2"),
                },
                "training_date": self.model_metadata.get("training_date"),
                "model_version": self.model_metadata.get("version"),
            })
        
        return info


# Global instance
prediction_service = None

def get_prediction_service() -> PredictionService:
    """Get or create prediction service."""
    global prediction_service
    if prediction_service is None:
        prediction_service = PredictionService()
    return prediction_service
