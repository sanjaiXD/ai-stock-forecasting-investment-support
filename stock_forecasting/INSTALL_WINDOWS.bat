@echo off
cls
echo ================================================================================
echo    AI STOCK FORECASTING - AUTOMATED INSTALLATION FOR WINDOWS
echo ================================================================================
echo.
echo This script will:
echo   1. Check Python installation
echo   2. Create virtual environment
echo   3. Install all dependencies
echo   4. Run system diagnostics
echo   5. Start the application
echo.
echo Press any key to start installation...
pause > nul
echo.

REM Check Python
echo ================================================================================
echo STEP 1: Checking Python...
echo ================================================================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python is installed
echo.

REM Create virtual environment
echo ================================================================================
echo STEP 2: Creating virtual environment...
echo ================================================================================
if exist venv (
    echo [INFO] Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo ================================================================================
echo STEP 3: Activating virtual environment...
echo ================================================================================
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo ================================================================================
echo STEP 4: Upgrading pip...
echo ================================================================================
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo ================================================================================
echo STEP 5: Installing dependencies (this may take 5-10 minutes)...
echo ================================================================================
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed!
    echo.
    echo Trying alternative installation method...
    echo Installing packages individually...
    
    pip install Flask==3.0.0
    pip install numpy==1.24.3
    pip install pandas==2.0.3
    pip install matplotlib==3.7.2
    pip install seaborn==0.12.2
    pip install scikit-learn==1.3.0
    pip install yfinance==0.2.28
    pip install flask-cors==4.0.0
    pip install Werkzeug==3.0.1
    
    echo Trying TensorFlow installation...
    pip install tensorflow==2.15.0
    
    if %errorlevel% neq 0 (
        echo TensorFlow standard version failed, trying CPU version...
        pip install tensorflow-cpu==2.15.0
    )
)
echo.
echo [OK] Dependencies installed
echo.

REM Create data directory
if not exist data mkdir data

REM Run diagnostics
echo ================================================================================
echo STEP 6: Running system diagnostics...
echo ================================================================================
python check_system.py
echo.

REM Success message
echo ================================================================================
echo    INSTALLATION COMPLETE!
echo ================================================================================
echo.
echo The application is ready to run!
echo.
echo Starting Flask server...
echo You can access the application at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ================================================================================
echo.

REM Run the application
python app.py

pause
