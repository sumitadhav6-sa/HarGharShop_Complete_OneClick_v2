@echo off
setlocal
cd /d "%~dp0"
title HarGharShop - One Click Starter

echo ================================================
echo          HarGharShop - One Click Setup
echo ================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python is not installed or not in PATH.
  echo Install Python 3.10+ and try again.
  pause
  exit /b 1
)
where npm >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Node.js/npm is not installed or not in PATH.
  echo Install Node.js LTS and try again.
  pause
  exit /b 1
)

if not exist "frontend\node_modules" (
  echo [1/3] Installing frontend packages...
  cd frontend
  call npm install
  if errorlevel 1 goto :fail
  cd ..
) else (
  echo [1/3] Frontend packages already installed.
)

echo [2/3] Installing backend packages...
cd backend
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail
cd ..

echo [3/3] Starting backend and frontend...
start "HarGharShop Backend" /D "%~dp0backend" cmd /k python app.py
timeout /t 2 /nobreak >nul
start "HarGharShop Frontend" /D "%~dp0frontend" cmd /k npm run dev
timeout /t 4 /nobreak >nul
start "" "http://localhost:5173"

echo.
echo HarGharShop is starting!
echo Frontend: http://localhost:5173
echo Backend : http://127.0.0.1:5000/api/health
echo.
echo Keep both black command windows open while using the website.
pause
exit /b 0

:fail
echo.
echo [ERROR] Setup failed. Read the error above.
pause
exit /b 1
