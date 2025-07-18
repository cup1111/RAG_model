@echo off
REM AI Code Assistant - Frontend Startup Script (Windows Version)
REM Author: Zane Wang
REM Email: 5finoilheater@gmail.com

setlocal enabledelayedexpansion

REM Parse command line arguments
set "check_only="
set "show_help="

:parse_args
if "%1"=="" goto :main
if "%1"=="--check-only" set "check_only=1"
if "%1"=="-h" set "show_help=1"
if "%1"=="--help" set "show_help=1"
shift
goto :parse_args

:show_help
echo ==========================================
echo     AI Code Assistant - Frontend Startup
echo ==========================================
echo.
echo Usage: start-frontend.bat [options]
echo.
echo Options:
echo   -h, --help      Show this help information
echo   --check-only    Check environment only, do not start service
echo.
echo Examples:
echo   start-frontend.bat          # Start frontend service
echo   start-frontend.bat --help   # Show help
echo   start-frontend.bat --check-only  # Check environment only
echo.
pause
exit /b 0

:check_environment_only
echo ==========================================
echo     AI Code Assistant - Environment Check
echo ==========================================
echo.
goto :check_environment

:main
if defined show_help goto :show_help
if defined check_only goto :check_environment_only

echo ==========================================
echo     AI Code Assistant - Frontend Startup
echo ==========================================
echo.

REM Check if in correct directory
if not exist "frontend" (
    echo [ERROR] Please run this script from the project root directory
    pause
    exit /b 1
)

:check_environment
REM Check Node.js version
echo [INFO] Checking Node.js version...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16.0.0 or higher first.
    echo [INFO] Download URL: https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set "node_version=%%i"
echo [SUCCESS] Node.js version check passed: !node_version!

REM Check npm
echo [INFO] Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm first.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set "npm_version=%%i"
echo [SUCCESS] npm version: !npm_version!

REM Check frontend directory
echo [INFO] Checking frontend project directory...
if not exist "frontend\package.json" (
    echo [ERROR] package.json file does not exist. Frontend project may be incomplete
    pause
    exit /b 1
)
echo [SUCCESS] Frontend project directory check passed

REM Install dependencies
echo [INFO] Checking and installing frontend dependencies...
cd frontend

if not exist "node_modules" (
    echo [WARNING] node_modules does not exist, installing dependencies...
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed successfully
) else (
    echo [INFO] Checking if dependencies need updating...
    npm install
    if errorlevel 1 (
        echo [ERROR] Failed to check dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependency check completed
)

cd ..

REM Check port availability (Windows)
echo [INFO] Checking if port 5173 is available...
netstat -an | findstr ":5173 " | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 5173 is already in use. Please close the program using this port
    echo [INFO] You can use the following command to see which process is using the port:
    echo [INFO] netstat -ano ^| findstr ":5173"
    pause
    exit /b 1
)
echo [SUCCESS] Port 5173 is available

if defined check_only (
    echo [SUCCESS] Environment check completed. All dependencies are ready!
    echo [INFO] You can now run start-frontend.bat to start the frontend service
    pause
    exit /b 0
)

REM Start frontend service
echo [INFO] Starting frontend service...
cd frontend

echo [SUCCESS] Frontend service starting...
echo [INFO] Service URL: http://localhost:5173
echo [INFO] Press Ctrl+C to stop the service
echo.
echo [INFO] Tip: Make sure the backend service is also running (http://localhost:3000)
echo.

REM Start development server
npm run dev

cd ..
pause 