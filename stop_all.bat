@echo off
REM ============================================================
REM  Sahayak AI - Stop All Services
REM ============================================================

echo.
echo ============================================================
echo   Stopping Sahayak AI Services
echo ============================================================
echo.

REM Stop Docker containers
echo [1/3] Stopping Cosdata container...
docker-compose down
echo [OK] Docker containers stopped
echo.

REM Kill FastAPI backend processes
echo [2/3] Stopping FastAPI backend...
taskkill /F /FI "WINDOWTITLE eq Sahayak Backend*" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
echo [OK] Backend stopped
echo.

REM Kill Streamlit frontend processes
echo [3/3] Stopping Streamlit frontend...
taskkill /F /FI "WINDOWTITLE eq Sahayak Frontend*" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do taskkill /F /PID %%a >nul 2>&1
echo [OK] Frontend stopped
echo.

echo ============================================================
echo   All Sahayak AI services stopped!
echo ============================================================
echo.
pause
