"""
Feature engineering for customer revenue prediction.
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional


class FeatureEngineer:
    """Feature engineering matching the notebook's exact logic."""
    
    REQUIRED_FEATURES = [
        'frequency', 'monetary_total', 'n_purchase_days', 'n_orders_items', 
        'recency', 'tenure_days', 'customer_age', 'aov', 
        'rev_30d', 'rev_90d', 'rev_180d', 'rev_365d',
        'revenue_growth_rate', 'revenue_trend_ratio',
        'freq_rate', 'maturity', 'recent_ratio',
        'avg_basket_rev', 'avg_basket_qty', 'avg_uniq_prods', 'max_order', 'order_cv',
        'n_orders', 'q4_frac', 'weekend_ratio', 'fav_dow', 
        'n_countries', 'is_uk', 'cancel_count', 'return_rate'
    ]
    
    def __init__(self):
        self.feature_count = len(self.REQUIRED_FEATURES)
    
    def engineer_from_dict(self, customer_data: Dict[str, Any]) -> pd.DataFrame:
        """Create feature vector from customer dictionary (API endpoint use)."""
        features = {}
        
        # Core RFM
        features['frequency'] = customer_data.get('frequency', 0)
        features['monetary_total'] = customer_data.get('monetary_total', 0.0)
        features['n_purchase_days'] = customer_data.get('n_purchase_days', 0)
        features['n_orders_items'] = customer_data.get('n_orders_items', 0)
        features['recency'] = customer_data.get('recency', 999)
        features['tenure_days'] = customer_data.get('tenure_days', 1)
        features['customer_age'] = customer_data.get('customer_age', 1)
        features['aov'] = (features['monetary_total'] / features['frequency'] 
                          if features['frequency'] > 0 else 0.0)
        
        # Temporal windows
        features['rev_30d'] = customer_data.get('rev_30d', 0.0)
        features['rev_90d'] = customer_data.get('rev_90d', 0.0)
        features['rev_180d'] = customer_data.get('rev_180d', 0.0)
        features['rev_365d'] = customer_data.get('rev_365d', 0.0)
        
        # Revenue trends
        r_recent = customer_data.get('rev_recent_90d', features['rev_90d'])
        r_prev = customer_data.get('rev_prev_90d', 0.0)
        features['revenue_growth_rate'] = min(10.0, max(-5.0, (r_recent - r_prev) / (r_prev + 1)))
        features['revenue_trend_ratio'] = (r_recent + 1) / (r_prev + 1)
        
        # Lifecycle
        features['freq_rate'] = features['frequency'] / (features['tenure_days'] + 1)
        features['maturity'] = features['n_purchase_days'] / (features['customer_age'] + 1)
        features['recent_ratio'] = features['rev_90d'] / (features['monetary_total'] + 1)
        
        # Basket
        features['avg_basket_rev'] = customer_data.get('avg_basket_rev', features['aov'])
        features['avg_basket_qty'] = customer_data.get('avg_basket_qty', 0.0)
        features['avg_uniq_prods'] = customer_data.get('avg_uniq_prods', 0.0)
        features['max_order'] = customer_data.get('max_order', features['monetary_total'])
        features['order_cv'] = customer_data.get('order_cv', 0.0)
        features['n_orders'] = customer_data.get('n_orders', features['frequency'])
        
        # Seasonality & behavior
        features['q4_frac'] = customer_data.get('q4_frac', 0.0)
        features['weekend_ratio'] = customer_data.get('weekend_ratio', 0.0)
        features['fav_dow'] = customer_data.get('fav_dow', 0)
        features['n_countries'] = customer_data.get('n_countries', 1)
        features['is_uk'] = int(customer_data.get('is_uk', True))
        
        # Returns
        features['cancel_count'] = customer_data.get('cancel_count', 0)
        features['return_rate'] = features['cancel_count'] / (features['frequency'] + 1)
        
        feature_df = pd.DataFrame([features])[self.REQUIRED_FEATURES]
        return feature_df
    
    def validate_features(self, features: pd.DataFrame) -> bool:
        """Validate feature DataFrame structure."""
        missing = set(self.REQUIRED_FEATURES) - set(features.columns)
        if missing:
            raise ValueError(f"Missing features: {missing}")
        if len(features) == 0:
            raise ValueError("Empty feature DataFrame")
        return True
