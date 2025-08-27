@echo off
echo ===========================================
echo  Photo Sorter - Simple Version (Fixed)
echo ===========================================
echo.

echo Starting Photo Sorter...
echo This version uses OpenCV face detection
echo and works without face-recognition library.
echo.

python main_simple_fixed.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo.
    echo Troubleshooting:
    echo 1. Make sure Python is installed
    echo 2. Install dependencies: pip install PyQt6 opencv-python numpy Pillow
    echo 3. Try running: python test_app.py
    echo.
    pause
) else (
    echo.
    echo Application closed successfully!
    echo.
)

pause


