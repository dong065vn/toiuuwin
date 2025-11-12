@echo off
:: Windows Optimizer Pro - Installation Script

echo ============================================
echo Windows Optimizer Pro - Installation
echo ============================================
echo.

:: Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
) else (
    echo [OK] Python is installed
    python --version
    echo.
)

:: Upgrade pip
echo [2/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

:: Install requirements
echo [3/4] Installing required packages...
echo.
echo Note: "Defaulting to user installation" is normal and not an error.
echo This happens when installing without admin rights.
echo.
pip install -r requirements.txt --user --upgrade
echo.

:: Test installation
echo [4/4] Testing installation...
python -c "import tkinter; import psutil; print('[OK] All packages installed successfully!')"
if %errorlevel% neq 0 (
    echo [ERROR] Package installation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo.

echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo To run the application:
echo   - Double-click "run_as_admin.bat" (Recommended)
echo   - Or run: python win_optimizer.py
echo.
echo Note: Some features require Administrator privileges
echo.
pause
