#!/bin/bash

# AI Stock Forecasting System - Startup Script

echo "============================================================"
echo "🚀 AI-Driven Stock Forecasting System"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed
    echo "✅ Dependencies installed"
    echo ""
fi

# Create data directory if it doesn't exist
mkdir -p data

echo "🌟 Starting Flask application..."
echo "📍 Application will be available at: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

# Run the application
python app.py
