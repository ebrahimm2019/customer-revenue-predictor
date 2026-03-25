"""Customer segmentation based on predicted revenue."""
from typing import Tuple, Dict
import numpy as np


class CustomerSegmenter:
    """Segment customers into VIP/High Value/Growth/At Risk."""
    
    SEGMENTS = {
        "VIP": {
            "threshold_min": 10000,
            "threshold_max": np.inf,
            "color": "#D4A853",
            "description": "Top-tier customers with exceptional value",
            "action": "White-glove service, exclusive offers, dedicated account manager"
        },
        "High Value": {
            "threshold_min": 2000,
            "threshold_max": 10000,
            "color": "#2D8659",
            "description": "High-spending customers with strong loyalty",
            "action": "Premium perks, early access, personalized recommendations"
        },
        "Growth": {
            "threshold_min": 500,
            "threshold_max": 2000,
            "color": "#3B82F6",
            "description": "Customers with growth potential",
            "action": "Engagement campaigns, upsell opportunities, loyalty incentives"
        },
        "At Risk": {
            "threshold_min": 0,
            "threshold_max": 500,
            "color": "#DC6843",
            "description": "Low-revenue or dormant customers at risk of churn",
            "action": "Re-engagement campaigns, win-back offers, feedback surveys"
        }
    }
    
    @classmethod
    def segment_customer(cls, predicted_revenue: float) -> Tuple[str, Dict]:
        """Determine segment from predicted revenue."""
        for segment_name, metadata in cls.SEGMENTS.items():
            if (predicted_revenue >= metadata["threshold_min"] and 
                predicted_revenue < metadata["threshold_max"]):
                return segment_name, metadata
        return "At Risk", cls.SEGMENTS["At Risk"]
    
    @classmethod
    def get_risk_level(cls, predicted_revenue: float, recency: int) -> str:
        """Determine risk level combining prediction and recency."""
        segment, _ = cls.segment_customer(predicted_revenue)
        
        if recency > 180 and predicted_revenue < 500:
            return "Critical"
        if recency > 90 or segment == "At Risk":
            return "High"
        if recency < 30 and predicted_revenue > 1000:
            return "Low"
        return "Medium"
