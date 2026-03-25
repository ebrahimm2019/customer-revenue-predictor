"""Train XGBoost model from notebook data."""
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb

# Config
DATA_DIR = Path(__file__).parent.parent
MODELS_DIR = DATA_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
SPLIT_DATE = pd.Timestamp('2011-10-01')

print("Loading data...")
df1 = pd.read_csv(DATA_DIR / "Year 2009-2010.csv", encoding='utf-8-sig')
df2 = pd.read_csv(DATA_DIR / "Year 2010-2011.csv", encoding='utf-8-sig')
df = pd.concat([df1, df2], ignore_index=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=False)
df['Revenue'] = df['Quantity'] * df['Price']
df['Invoice'] = df['Invoice'].astype(str)

# Clean
df = df[df['Customer ID'].notna()]
df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]
df = df[(df['Quantity'] <= 20000) & (df['Price'] <= 1000)]

cal_df = df[df['InvoiceDate'] < SPLIT_DATE].copy()
holdout_df = df[df['InvoiceDate'] >= SPLIT_DATE].copy()
cancel_df = df[df['Invoice'].str.startswith('C')].copy()

print(f"Engineering features for {df['Customer ID'].nunique():,} customers...")

# Feature engineering (condensed)
def engineer_features(trans_df, cutoff_date, cancel_trans=None):
    df_local = trans_df[trans_df['InvoiceDate'] < cutoff_date].copy()
    rfm = df_local.groupby('Customer ID').agg(
        frequency=('Invoice', 'nunique'), monetary_total=('Revenue', 'sum'),
        last_purchase=('InvoiceDate', 'max'), first_purchase=('InvoiceDate', 'min'),
        n_purchase_days=('InvoiceDate', lambda x: x.dt.date.nunique()),
        n_orders_items=('Quantity', 'sum'),
    ).reset_index()
    rfm['recency'] = (cutoff_date - rfm['last_purchase']).dt.days
    rfm['tenure_days'] = (rfm['last_purchase'] - rfm['first_purchase']).dt.days + 1
    rfm['customer_age'] = (cutoff_date - rfm['first_purchase']).dt.days
    rfm['aov'] = rfm['monetary_total'] / rfm['frequency']
    for days in [30, 90, 180, 365]:
        w = cutoff_date - timedelta(days=days)
        r = df_local[df_local['InvoiceDate'] >= w].groupby('Customer ID')['Revenue'].sum().rename(f'rev_{days}d')
        rfm = rfm.merge(r, on='Customer ID', how='left')
        rfm[f'rev_{days}d'] = rfm[f'rev_{days}d'].fillna(0)
    mid = cutoff_date - timedelta(days=90)
    prev_start = mid - timedelta(days=90)
    r_rec = df_local[df_local['InvoiceDate'] >= mid].groupby('Customer ID')['Revenue'].sum().rename('r_rec')
    r_prev = df_local[(df_local['InvoiceDate'] >= prev_start) & (df_local['InvoiceDate'] < mid)].groupby('Customer ID')['Revenue'].sum().rename('r_prev')
    rfm = rfm.merge(r_rec, on='Customer ID', how='left').merge(r_prev, on='Customer ID', how='left')
    rfm['revenue_growth_rate'] = ((rfm['r_rec'] - rfm['r_prev']) / (rfm['r_prev'] + 1)).fillna(0).clip(-5, 10)
    rfm['revenue_trend_ratio'] = (rfm['r_rec'] + 1) / (rfm['r_prev'] + 1)
    rfm['freq_rate'] = rfm['frequency'] / (rfm['tenure_days'] + 1)
    rfm['maturity'] = rfm['n_purchase_days'] / (rfm['customer_age'] + 1)
    rfm['recent_ratio'] = rfm['rev_90d'] / (rfm['monetary_total'] + 1)
    basket = df_local.groupby(['Customer ID','Invoice']).agg(b_rev=('Revenue', 'sum'), b_qty=('Quantity', 'sum'), b_prods=('StockCode', 'nunique')).groupby('Customer ID').agg(avg_basket_rev=('b_rev', 'mean'), avg_basket_qty=('b_qty', 'mean'), avg_uniq_prods=('b_prods', 'mean'), max_order=('b_rev', 'max'), order_cv=('b_rev', lambda x: x.std()/(x.mean()+1)), n_orders=('b_rev', 'count')).reset_index()
    rfm = rfm.merge(basket, on='Customer ID', how='left')
    df_local['is_q4'] = df_local['InvoiceDate'].dt.month.isin([10,11,12])
    q4 = df_local.groupby('Customer ID').apply(lambda x: x.loc[x['is_q4'],'Revenue'].sum() / (x['Revenue'].sum() + 1)).rename('q4_frac').reset_index()
    rfm = rfm.merge(q4, on='Customer ID', how='left')
    df_local['dow'] = df_local['InvoiceDate'].dt.dayofweek
    beh = df_local.groupby('Customer ID').agg(weekend_ratio=('dow', lambda x: (x >= 5).mean()), fav_dow=('dow', lambda x: x.mode()[0] if len(x.mode()) else 0), n_countries=('Country', 'nunique')).reset_index()
    beh['is_uk'] = df_local.groupby('Customer ID')['Country'].apply(lambda x: (x == 'United Kingdom').mean() > 0.5).astype(int).values
    rfm = rfm.merge(beh, on='Customer ID', how='left')
    if cancel_trans is not None:
        ret = cancel_trans[cancel_trans['Customer ID'].notna()].groupby('Customer ID')['Invoice'].nunique().rename('cancel_count').reset_index()
        rfm = rfm.merge(ret, on='Customer ID', how='left')
        rfm['cancel_count'] = rfm['cancel_count'].fillna(0)
        rfm['return_rate'] = rfm['cancel_count'] / (rfm['frequency'] + 1)
    rfm = rfm.fillna(0).set_index('Customer ID')
    rfm = rfm.drop(columns=[c for c in ['last_purchase','first_purchase','r_rec','r_prev'] if c in rfm.columns])
    return rfm

X_train = engineer_features(cal_df, SPLIT_DATE, cancel_df)
y_actual = holdout_df.groupby('Customer ID')['Revenue'].sum()
y_train = y_actual.reindex(X_train.index, fill_value=0)

print(f"Training XGBoost on {X_train.shape[0]:,} customers with {X_train.shape[1]} features...")
model = xgb.XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, min_child_weight=3, gamma=0.1, random_state=42, verbosity=0)
model.fit(X_train, y_train)

y_pred = model.predict(X_train)
rmse = np.sqrt(mean_squared_error(y_train, y_pred))
mae = mean_absolute_error(y_train, y_pred)
r2 = r2_score(y_train, y_pred)

print(f"\n✓ Model Performance:")
print(f"  RMSE: £{rmse:,.2f}")
print(f"  MAE:  £{mae:,.2f}")
print(f"  R²:   {r2:.4f}")

# Save
with open(MODELS_DIR / "trained_model.pkl", 'wb') as f:
    pickle.dump(model, f)
with open(MODELS_DIR / "model_metadata.json", 'w') as f:
    json.dump({"model_type": "XGBRegressor", "version": "1.0.0", "training_date": datetime.now().isoformat(), "rmse": float(rmse), "mae": float(mae), "r2": float(r2)}, f, indent=2)

print(f"\n✅ Model saved to {MODELS_DIR}/trained_model.pkl")
print(f"Ready to run: uv run uvicorn app.main:app --reload")
