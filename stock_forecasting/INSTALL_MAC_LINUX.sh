#!/bin/bash

clear
echo "================================================================================"
echo "   AI STOCK FORECASTING - AUTOMATED INSTALLATION FOR MAC/LINUX"
echo "================================================================================"
echo ""
echo "This script will:"
echo "  1. Check Python installation"
echo "  2. Create virtual environment"
echo "  3. Install all dependencies"
echo "  4. Run system diagnostics"
echo "  5. Start the application"
echo ""
read -p "Press Enter to start installation..."
echo ""

# Check Python
echo "================================================================================"
echo "STEP 1: Checking Python..."
echo "================================================================================"

if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PIP_CMD=pip
else
    echo ""
    echo "[ERROR] Python is not installed!"
    echo ""
    echo "Please install Python 3.8+ from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

$PYTHON_CMD --version
echo "[OK] Python is installed"
echo ""

# Create virtual environment
echo "================================================================================"
echo "STEP 2: Creating virtual environment..."
echo "================================================================================"

if [ -d "venv" ]; then
    echo "[INFO] Virtual environment already exists"
else
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[OK] Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "================================================================================"
echo "STEP 3: Activating virtual environment..."
echo "================================================================================"

source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi
echo "[OK] Virtual environment activated"
echo ""

# Upgrade pip
echo "================================================================================"
echo "STEP 4: Upgrading pip..."
echo "================================================================================"
pip install --upgrade pip
echo ""

# Install dependencies
echo "================================================================================"
echo "STEP 5: Installing dependencies (this may take 5-10 minutes)..."
echo "================================================================================"

pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Installation failed!"
    echo ""
    echo "Trying alternative installation method..."
    echo "Installing packages individually..."
    
    pip install Flask==3.0.0
    pip install numpy==1.24.3
    pip install pandas==2.0.3
    pip install matplotlib==3.7.2
    pip install seaborn==0.12.2
    pip install scikit-learn==1.3.0
    pip install yfinance==0.2.28
    pip install flask-cors==4.0.0
    pip install Werkzeug==3.0.1
    
    echo "Trying TensorFlow installation..."
    pip install tensorflow==2.15.0
    
    if [ $? -ne 0 ]; then
        echo "TensorFlow standard version failed, trying CPU version..."
        pip install tensorflow-cpu==2.15.0
    fi
fi

echo ""
echo "[OK] Dependencies installed"
echo ""

# Create data directory
mkdir -p data

# Run diagnostics
echo "================================================================================"
echo "STEP 6: Running system diagnostics..."
echo "================================================================================"
python check_system.py
echo ""

# Success message
echo "================================================================================"
echo "   INSTALLATION COMPLETE!"
echo "================================================================================"
echo ""
echo "The application is ready to run!"
echo ""
echo "Starting Flask server..."
echo "You can access the application at: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================================================"
echo ""

# Run the application
python app.py
