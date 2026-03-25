#!/bin/bash

echo "============================================================"
echo "  Customer Revenue Predictor - Starting Server"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "   uv sync"
    echo ""
    exit 1
fi

# Check if model exists
if [ ! -f "models/trained_model.pkl" ]; then
    echo "[WARNING] Model not found!"
    echo ""
    echo "Please train the model first:"
    echo "   uv run python scripts/train_model.py"
    echo ""
    read -p "Press Enter to continue anyway, or CTRL+C to stop..."
fi

echo "Starting server..."
echo ""
echo "Server will be available at: http://localhost:8000"
echo "Press CTRL+C to stop"
echo ""

# Run the server
uv run python run.py
