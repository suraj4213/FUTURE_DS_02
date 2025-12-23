@echo off
setlocal enabledelayedexpansion

REM Navigate to repository root (folder of this script)
cd /d "%~dp0"

echo ==================================================
echo Running Social Media Campaign data pipeline...
echo ==================================================

python data_generator.py
if errorlevel 1 goto :error

python data_cleaner.py
if errorlevel 1 goto :error

python metrics_calculator.py
if errorlevel 1 goto :error

echo.
echo ==================================================
echo Launching local web dashboard on http://localhost:8000/web/
echo Press CTRL+C to stop the server when finished.
echo ==================================================
echo.

start "" "http://localhost:8000/web/"
python -m http.server 8000
goto :eof

:error
echo.
echo Pipeline failed. Check the messages above for details.
exit /b 1