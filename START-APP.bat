@echo off
title CropGuard AI v3 - Launcher
color 0A
echo.
echo  ============================================================
echo    CropGuard AI v3 - Visakhapatnam Edition
echo    Starting all services...
echo  ============================================================
echo.

REM Start MongoDB if not running
echo  [1/3] Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul 2>&1
if %errorlevel% neq 0 (
    echo  Starting MongoDB service...
    net start MongoDB >nul 2>&1
    timeout /t 3 /nobreak >nul
)
echo  [OK] MongoDB is running
echo.

REM Start Backend
echo  [2/3] Starting Backend Server (FastAPI)...
start "CropGuard Backend" cmd /k "title CropGuard Backend && color 0A && cd /d %~dp0backend && call venv\Scripts\activate.bat && echo Backend starting... && uvicorn app.main:app --reload --port 8000 --host 0.0.0.0"
echo  Waiting for backend to be ready...
timeout /t 6 /nobreak >nul
echo  [OK] Backend started at http://localhost:8000
echo.

REM Start Frontend
echo  [3/3] Starting Frontend (React)...
start "CropGuard Frontend" cmd /k "title CropGuard Frontend && color 0A && cd /d %~dp0frontend && echo Frontend starting... && npm run dev"
echo  Waiting for frontend to be ready...
timeout /t 8 /nobreak >nul
echo  [OK] Frontend started
echo.

REM Open browser
echo  Opening browser...
start "" "http://localhost:5173"

echo.
echo  ============================================================
echo    CropGuard AI is RUNNING!
echo.
echo    App URL  : http://localhost:5173
echo    API Docs : http://localhost:8000/docs
echo.
echo    Two windows opened - keep them running.
echo    Close this window when done.
echo  ============================================================
echo.
pause
