@echo off
echo Starting Photo Sorter with debug output...
cd /d %~dp0
python main_simple.py
echo.
echo If the application doesn't show or you see a white screen,
echo check the error messages above.
pause
