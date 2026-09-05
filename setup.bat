@echo off
title CropGuard AI v3 - Setup
color 0A
echo.
echo  ============================================================
echo    CropGuard AI v3 - MongoDB Edition - Visakhapatnam
echo    Setup Script
echo  ============================================================
echo.

REM ── Check Python ──────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found!
    echo  Please install Python from: https://python.org/downloads
    echo  IMPORTANT: Tick "Add Python to PATH" during install!
    echo.
    pause
    exit /b 1
)
echo  [OK] Python found
echo.

REM ── Check Node.js ─────────────────────────────────────────────
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Node.js not found!
    echo  Please install Node.js from: https://nodejs.org
    echo  Download the LTS version.
    echo.
    pause
    exit /b 1
)
echo  [OK] Node.js found
echo.

REM ── Check MongoDB ─────────────────────────────────────────────
echo  [CHECKING] MongoDB...
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  [INFO] MongoDB not found as command - checking if service is running...
    sc query MongoDB >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo  ============================================================
        echo   MongoDB is not installed. Please install it first:
        echo.
        echo   1. Go to: https://www.mongodb.com/try/download/community
        echo   2. Choose: Windows, Version 7.0, MSI package
        echo   3. Click Download and install
        echo   4. IMPORTANT: During install, check "Install MongoD as a Service"
        echo   5. After install, run this setup.bat again
        echo  ============================================================
        echo.
        pause
        exit /b 1
    )
)
echo  [OK] MongoDB found
echo.

REM ── Install Python packages ────────────────────────────────────
echo  [1/3] Installing Python backend packages...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to install Python packages
    pause
    exit /b 1
)
echo  [OK] Python packages installed
echo.
call venv\Scripts\deactivate.bat
cd ..

REM ── Install Node packages ──────────────────────────────────────
echo  [2/3] Installing frontend packages...
cd frontend
call npm install --silent
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to install Node packages
    pause
    exit /b 1
)
echo  [OK] Node packages installed
echo.
cd ..

REM ── Create uploads folder ──────────────────────────────────────
echo  [3/3] Creating uploads folder...
if not exist "backend\uploads" mkdir backend\uploads
echo  [OK] Uploads folder ready
echo.

echo  ============================================================
echo    Setup Complete!
echo.
echo    To START the app, just double-click:
echo    >>> START-APP.bat <<<
echo.
echo    It will open http://localhost:5173 automatically
echo  ============================================================
echo.
pause
