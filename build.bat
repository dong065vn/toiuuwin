@echo off
:: Windows Optimizer Pro - Build Script
:: Tạo file EXE từ Python code

echo ============================================
echo Windows Optimizer Pro - Build EXE
echo ============================================
echo.

:: Check if PyInstaller is installed
echo [1/4] Kiểm tra PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] PyInstaller chưa được cài đặt
    echo [*] Đang cài đặt PyInstaller...
    pip install pyinstaller --user
    echo.
) else (
    echo [OK] PyInstaller đã sẵn sàng
    echo.
)

:: Clean old build
echo [2/4] Dọn dẹp bản build cũ...
if exist "dist" rd /s /q dist
if exist "build" rd /s /q build
if exist "*.spec" del /q *.spec
echo.

:: Build EXE
echo [3/4] Đang build file EXE...
echo Quá trình này có thể mất vài phút, vui lòng chờ...
echo.

pyinstaller --name="WindowsOptimizerPro" ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data="README.md;." ^
    --hidden-import=tkinter ^
    --hidden-import=psutil ^
    --clean ^
    win_optimizer.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build thất bại!
    echo Vui lòng kiểm tra lỗi ở trên.
    pause
    exit /b 1
)

echo.
echo [4/4] Kiểm tra file đã build...
if exist "dist\WindowsOptimizerPro.exe" (
    echo.
    echo ============================================
    echo Build thành công!
    echo ============================================
    echo.
    echo File EXE đã được tạo tại:
    echo   dist\WindowsOptimizerPro.exe
    echo.
    echo Kích thước file:
    dir "dist\WindowsOptimizerPro.exe" | findstr "WindowsOptimizerPro.exe"
    echo.
    echo Bạn có thể sao chép file này ra ngoài và chạy độc lập
    echo mà không cần cài đặt Python!
    echo.
) else (
    echo [ERROR] Không tìm thấy file EXE!
    pause
    exit /b 1
)

echo Dọn dẹp file tạm...
if exist "build" rd /s /q build
if exist "*.spec" del /q *.spec

echo.
echo ============================================
echo Hoàn thành!
echo ============================================
echo.
pause
