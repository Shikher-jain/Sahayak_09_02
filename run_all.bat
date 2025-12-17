@echo off
REM ============================================================
REM  Sahayak AI - Complete Project Startup Script
REM ============================================================
REM  This script starts the entire Sahayak project:
REM  1. Cosdata Vector DB (Docker)
REM  2. FastAPI Backend
REM  3. Streamlit Frontend
REM ============================================================

echo.
echo ============================================================
echo   Starting Sahayak AI Teaching Assistant
echo ============================================================
echo.

REM Check if Docker is running
echo [1/5] Checking Docker status...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker is running
echo.

REM Start Cosdata container
echo [2/5] Starting Cosdata Vector DB...
docker-compose up -d cosdata
if errorlevel 1 (
    echo [ERROR] Failed to start Cosdata container
    pause
    exit /b 1
)
echo [OK] Cosdata container started
echo.

REM Wait for Cosdata to be ready
echo [3/5] Waiting for Cosdata to be ready (10 seconds)...
timeout /t 10 /nobreak >nul
echo [OK] Cosdata should be ready
echo.

REM Start FastAPI backend in new window
echo [4/5] Starting FastAPI Backend...
start "Sahayak Backend" cmd /k "cd /d %~dp0 && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul
echo [OK] Backend started in new window
echo.

REM Start Streamlit frontend in new window
echo [5/5] Starting Streamlit Frontend...
start "Sahayak Frontend" cmd /k "cd /d %~dp0 && streamlit run frontend/app.py"
timeout /t 3 /nobreak >nul
echo [OK] Frontend started in new window
echo.

echo ============================================================
echo   Sahayak AI is now running!
echo ============================================================
echo.
echo   Cosdata Vector DB:  http://localhost:8443
echo   FastAPI Backend:    http://localhost:8000
echo   Streamlit Frontend: http://localhost:8501
echo.
echo   Backend API Docs:   http://localhost:8000/docs
echo   Health Check:       http://localhost:8000/health
echo.
echo ============================================================
echo   Press any key to open the application in your browser...
echo ============================================================
pause >nul

REM Open frontend in browser
start http://localhost:8501

echo.
echo Application opened in browser!
echo.
echo To stop all services, close the terminal windows or run:
echo   stop_all.bat
echo.
pause
