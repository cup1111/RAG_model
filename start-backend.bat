@echo off
REM AI Code Assistant - Backend Startup Script (Windows Version)
REM Author: Zane Wang
REM Email: 5finoilheater@gmail.com

setlocal enabledelayedexpansion

echo ==========================================
echo     AI Code Assistant - Backend Startup
echo ==========================================
echo.

REM Check if in correct directory
if not exist "python-backend" (
    echo [ERROR] Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check Python version
echo [INFO] Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher first.
    pause
    exit /b 1
)

REM Check virtual environment
echo [INFO] Checking virtual environment...
if not exist "python-backend\venv" (
    echo [WARNING] Virtual environment does not exist, creating...
    cd python-backend
    python -m venv venv
    echo [SUCCESS] Virtual environment created successfully
    cd ..
) else (
    echo [SUCCESS] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call python-backend\venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated

REM Install dependencies
echo [INFO] Checking and installing Python dependencies...
cd python-backend
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt file does not exist
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
cd ..
echo [SUCCESS] Dependencies installed successfully

REM Check environment variables
echo [INFO] Checking environment variable configuration...
if not exist "python-backend\.env" (
    echo [WARNING] .env file does not exist, creating...
    echo OPENAI_API_KEY=your_openai_api_key_here > python-backend\.env
    echo [WARNING] Please edit python-backend\.env file to set your OpenAI API key
    echo [WARNING] Format: OPENAI_API_KEY=sk-your-actual-api-key
) else (
    echo [SUCCESS] .env file already exists
)

REM Start backend service
echo [INFO] Starting backend service...
cd python-backend

if not exist "main.py" (
    echo [ERROR] main.py file does not exist
    pause
    exit /b 1
)

echo [SUCCESS] Backend service starting...
echo [INFO] Service URL: http://localhost:3000
echo [INFO] API Documentation: http://localhost:3000/docs
echo [INFO] Press Ctrl+C to stop the service
echo.

REM Start the service
python main.py

cd ..
pause 