@echo off
setlocal
cd /d "%~dp0"
title HarGharShop - One Server

echo Building frontend...
if not exist "frontend\node_modules" (
  cd frontend
  call npm install
  if errorlevel 1 goto :fail
  cd ..
)
cd frontend
call npm run build
if errorlevel 1 goto :fail
cd ..
echo.
echo Build complete. Starting backend server...
cd backend
python app.py
exit /b
:fail
echo Build/setup failed.
pause
