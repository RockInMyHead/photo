@echo off
echo ===========================================
echo  Photo Sorter - Quick Installation
echo ===========================================
echo.

echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo.

echo Installing dependencies...
echo This may take a few minutes...
echo.

REM Try the smart installer first
python install_deps.py

if errorlevel 1 (
    echo.
    echo Smart installer failed, trying manual installation...
    echo.

    REM Install packages one by one
    echo Installing PyQt6...
    pip install PyQt6

    echo Installing OpenCV...
    pip install opencv-python

    echo Installing NumPy...
    pip install numpy

    echo Installing Pillow...
    pip install Pillow

    echo Installing Face Recognition...
    pip install face-recognition

    echo Installing CMake...
    pip install cmake
)

echo.
echo ===========================================
echo  Installation completed!
echo ===========================================
echo.
echo To run the application:
echo   python main.py
echo.
echo Or use the launcher:
echo   python run.py
echo.
echo ===========================================
pause


