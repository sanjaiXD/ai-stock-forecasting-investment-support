@echo off
echo ============================================================
echo 🚀 AI-Driven Stock Forecasting System
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
if not exist "venv\installed" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    echo installed > venv\installed
    echo ✅ Dependencies installed
    echo.
)

REM Create data directory if it doesn't exist
if not exist "data\" mkdir data

echo 🌟 Starting Flask application...
echo 📍 Application will be available at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Run the application
python app.py

pause
