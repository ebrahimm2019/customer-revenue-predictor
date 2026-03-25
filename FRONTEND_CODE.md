# Frontend Implementation Guide

Due to size constraints, here's the architecture for the frontend files.
Create these files in `app/static/`:

## File Structure
```
app/static/
├── index.html          # Landing page
├── dashboard.html      # Main dashboard
├── predict.html        # Prediction interface
├── insights.html       # Model insights
├── css/
│   └── style.css      # Unified styles
└── js/
    ├── dashboard.js    # Dashboard logic
    ├── predict.js      # Prediction form
    └── utils.js        # Shared utilities
```

## Design System (from CustomerSalesDashboard.jsx)

### Colors
```css
:root {
  --bg: #0C0F1A;
  --surface: #141828;
  --text: #E8E9F0;
  --text2: #9BA1B8;
  --accent: #D4A853;  /* Gold - VIP */
  --blue: #3B82F6;    /* Blue - Growth */
  --green: #2D8659;   /* Green - High Value */
  --orange: #DC6843;  /* Orange - At Risk */
}
```

### Typography
- Font: DM Sans (body), Fraunces (display)
- Sizes: 11-14px body, 18-24px headings

### Components
1. **Stat Cards** - KPIs with icons, large numbers, trend indicators
2. **Segment Pills** - Color-coded customer segments
3. **Charts** - Revenue curves, distributions, time series
4. **Forms** - Customer feature inputs with validation
5. **Results Cards** - Predictions with confidence intervals

## Key Pages

### 1. index.html (Landing)
- Hero section with value proposition
- Quick stats (customers analyzed, accuracy, segments)
- CTA buttons → Dashboard, Predict
- Feature highlights

### 2. dashboard.html (Main Interface)
- **Top KPIs**: Total customers, predicted revenue, avg/median
- **Segment Cards**: VIP/High Value/Growth/At Risk counts
- **Revenue Chart**: Monthly predicted revenue
- **Customer Table**: Sortable, filterable list

### 3. predict.html (Prediction Form)
- **Simple Form**: 8 key inputs (frequency, monetary, recency, revenue windows)
- **Advanced Toggle**: All 30 features
- **Result Card**: Shows prediction, confidence, segment, insights
- **Batch Upload**: CSV upload for bulk predictions

### 4. insights.html (Model Info)
- **Feature Importance**: Bar chart of top 10 drivers
- **Model Metrics**: RMSE, MAE, R² in cards
- **Business Translation**: Explain features in plain language
- **Confidence Notes**: How to interpret predictions

## API Integration Pattern

```javascript
// Fetch prediction
async function predict(customerData) {
  const res = await fetch('/api/predict/single', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(customerData)
  });
  return await res.json();
}

// Render result
function showResult(data) {
  document.getElementById('prediction').innerHTML = `
    <div class="result-card" style="border-left: 4px solid ${data.segment_color}">
      <h3>£${data.predicted_revenue.toFixed(0)}</h3>
      <p>${data.segment} Customer</p>
      <div class="confidence">
        Range: £${data.confidence_interval.lower.toFixed(0)} - 
              £${data.confidence_interval.upper.toFixed(0)}
      </div>
      <div class="insights">
        ${data.insights.map(i => `<p>${i}</p>`).join('')}
      </div>
    </div>
  `;
}
```

## Quick Implementation

Since full frontend code is extensive, you have 3 options:

### Option A: Minimal HTML (Fastest)
Create basic forms that POST to API and display JSON. Add CSS later.

### Option B: Copy Reference UI
Adapt the CustomerSalesDashboard.jsx patterns to vanilla HTML/JS/CSS.

### Option C: Use Framework
Build with React/Vue and call the FastAPI backend as an API.

**Recommendation:** Start with Option A for MVP, then enhance.

## Sample predict.html (Minimal)

```html
<!DOCTYPE html>
<html>
<head>
  <title>Predict Revenue</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
    input { width: 100%; padding: 8px; margin: 5px 0; }
    button { background: #3B82F6; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    .result { margin-top: 20px; padding: 20px; background: #f5f5f5; border-radius: 8px; }
  </style>
</head>
<body>
  <h1>Customer Revenue Prediction</h1>
  
  <form id="predictForm">
    <label>Frequency (# purchases):</label>
    <input type="number" id="frequency" required>
    
    <label>Total Spending (£):</label>
    <input type="number" id="monetary_total" step="0.01" required>
    
    <label>Recency (days since last purchase):</label>
    <input type="number" id="recency" required>
    
    <label>Revenue last 90 days (£):</label>
    <input type="number" id="rev_90d" step="0.01">
    
    <label>UK Customer:</label>
    <input type="checkbox" id="is_uk" checked>
    
    <button type="submit">Predict</button>
  </form>
  
  <div id="result" class="result" style="display:none;"></div>
  
  <script>
    document.getElementById('predictForm').onsubmit = async (e) => {
      e.preventDefault();
      const data = {
        frequency: parseInt(document.getElementById('frequency').value),
        monetary_total: parseFloat(document.getElementById('monetary_total').value),
        recency: parseInt(document.getElementById('recency').value),
        rev_90d: parseFloat(document.getElementById('rev_90d').value) || 0,
        is_uk: document.getElementById('is_uk').checked
      };
      
      const res = await fetch('/api/predict/single', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      
      const result = await res.json();
      
      document.getElementById('result').style.display = 'block';
      document.getElementById('result').innerHTML = `
        <h2>Prediction: £${result.predicted_revenue.toFixed(2)}</h2>
        <p><strong>Segment:</strong> ${result.segment}</p>
        <p><strong>Risk Level:</strong> ${result.risk_level}</p>
        <p><strong>Confidence Range:</strong> £${result.confidence_interval.lower.toFixed(2)} - £${result.confidence_interval.upper.toFixed(2)}</p>
        <h3>Insights:</h3>
        ${result.insights.map(i => `<p>• ${i}</p>`).join('')}
        <p><strong>Recommended Action:</strong> ${result.recommended_action}</p>
      `;
    };
  </script>
</body>
</html>
```

Create similar files for index.html, dashboard.html, insights.html with API calls to respective endpoints.
