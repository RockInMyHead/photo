@echo off
echo ===========================================
echo  Photo Sorter - Optimized Version
echo ===========================================
echo.

echo Starting optimized version...
echo This version is fast and won't hang!
echo.

python photo_sorter_optimized.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo.
    echo Make sure you have installed dependencies:
    echo pip install -r requirements.txt
    echo.
    pause
) else (
    echo.
    echo Application closed successfully!
    echo.
)

pause


