"""
Main FastAPI application for Customer Revenue Predictor.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import sys
from pathlib import Path

# Add parent directory to path for direct execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from .config import settings
    from .api import router
except ImportError:
    from app.config import settings
    from app.api import router

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# Include API routes
app.include_router(router, prefix="/api", tags=["predictions"])


# Root endpoint - serve main page
@app.get("/")
async def root():
    """Serve the main dashboard page."""
    return FileResponse(settings.STATIC_DIR / "index.html")


@app.get("/dashboard")
async def dashboard():
    """Serve dashboard page."""
    return FileResponse(settings.STATIC_DIR / "dashboard.html")


@app.get("/predict")
async def predict_page():
    """Serve prediction page."""
    return FileResponse(settings.STATIC_DIR / "predict.html")


@app.get("/insights")
async def insights_page():
    """Serve insights page."""
    return FileResponse(settings.STATIC_DIR / "insights.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
