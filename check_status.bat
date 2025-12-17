@echo off
REM ============================================================
REM  Sahayak AI - Quick Status Check
REM ============================================================

echo.
echo ============================================================
echo   Sahayak AI - Service Status
echo ============================================================
echo.

REM Check Docker
echo [Docker Status]
docker info >nul 2>&1
if errorlevel 1 (
    echo   Docker: NOT RUNNING
) else (
    echo   Docker: RUNNING
)
echo.

REM Check Cosdata container
echo [Cosdata Vector DB - Port 8443]
docker ps | findstr cosdata >nul 2>&1
if errorlevel 1 (
    echo   Cosdata: NOT RUNNING
) else (
    echo   Cosdata: RUNNING
)
netstat -an | findstr :8443 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo   Port 8443: NOT LISTENING
) else (
    echo   Port 8443: LISTENING
)
echo.

REM Check Backend
echo [FastAPI Backend - Port 8000]
netstat -an | findstr :8000 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo   Backend: NOT RUNNING
    echo   Port 8000: NOT LISTENING
) else (
    echo   Backend: RUNNING
    echo   Port 8000: LISTENING
)
echo.

REM Check Frontend
echo [Streamlit Frontend - Port 8501]
netstat -an | findstr :8501 | findstr LISTENING >nul 2>&1
if errorlevel 1 (
    echo   Frontend: NOT RUNNING
    echo   Port 8501: NOT LISTENING
) else (
    echo   Frontend: RUNNING
    echo   Port 8501: LISTENING
)
echo.

echo ============================================================
echo   Quick Access Links
echo ============================================================
echo   Frontend:     http://localhost:8501
echo   Backend API:  http://localhost:8000
echo   API Docs:     http://localhost:8000/docs
echo   Health:       http://localhost:8000/health
echo ============================================================
echo.
pause
