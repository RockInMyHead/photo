@echo off
echo Запуск Photo Sorter...
cd /d %~dp0
python main_simple.py
echo.
echo Если приложение не запустилось, проверьте ошибки выше.
pause
