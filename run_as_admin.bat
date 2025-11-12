@echo off
:: Windows Optimizer Pro - Run as Administrator
:: This batch file automatically requests administrator privileges

echo ============================================
echo Windows Optimizer Pro
echo Professional System Optimization Tool
echo ============================================
echo.

:: Check for administrator privileges
net session >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Running with Administrator privileges
    echo.
    goto :run
) else (
    echo [!] Not running as Administrator
    echo [*] Requesting Administrator privileges...
    echo.

    :: Request administrator privileges
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run
echo [*] Starting Windows Optimizer Pro...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo [*] Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check if required packages are installed
echo [*] Checking dependencies...
python -c "import psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Installing required packages...
    pip install -r requirements.txt
    echo.
)

:: Run the application
echo [*] Launching application...
echo.
python win_optimizer.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application encountered an error
    pause
)

exit /b
