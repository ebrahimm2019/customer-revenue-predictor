@echo off
echo ============================================================
echo   Customer Revenue Predictor - Starting Server
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first:
    echo    uv sync
    echo.
    pause
    exit /b 1
)

REM Check if model exists
if not exist "models\trained_model.pkl" (
    echo [WARNING] Model not found!
    echo.
    echo Please train the model first:
    echo    uv run python scripts\train_model.py
    echo.
    echo Press any key to continue anyway, or CTRL+C to stop...
    pause
)

echo Starting server...
echo.
echo Server will be available at: http://localhost:8000
echo Press CTRL+C to stop
echo.

REM Run the server
uv run python run.py
