@echo off
:: Chay WindowsOptimizerPro voi console de xem output
echo ============================================================
echo WINDOWS OPTIMIZER PRO v6.0 - Running with Console
echo ============================================================
echo.

cd /d "%~dp0dist"

echo Starting app with Administrator rights...
echo.

:: Chay voi admin rights va giu console
powershell -Command "Start-Process 'WindowsOptimizerPro_v6.0.exe' -Verb RunAs"

echo.
echo App started! Check for UAC prompt.
echo.
pause
