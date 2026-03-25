"""
Startup script for Customer Revenue Predictor.
Run this file directly or use uvicorn.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    print("="*60)
    print("🚀 Starting Customer Revenue Predictor")
    print("="*60)
    print("\n📍 Server will be available at:")
    print("   http://localhost:8000")
    print("\n📊 Available pages:")
    print("   • Landing:    http://localhost:8000/")
    print("   • Dashboard:  http://localhost:8000/dashboard")
    print("   • Predict:    http://localhost:8000/predict")
    print("   • Insights:   http://localhost:8000/insights")
    print("\n🔌 API Documentation:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc:      http://localhost:8000/redoc")
    print("\n" + "="*60)
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
