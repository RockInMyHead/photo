@echo off
echo Starting Photo Sorter Application...
echo.

REM Try to run the application
python run.py

if errorlevel 1 (
    echo Error: Failed to run with python
    echo Trying with python3...
    python3 run.py
)

if errorlevel 1 (
    echo Error: Failed to run with python3
    echo Please make sure Python is installed and in PATH
    echo You can also try running: python main.py
    pause
) else (
    echo Application started successfully!
)

pause

