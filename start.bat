@echo off
chcp 65001 >nul
echo Photo Sorter - Запуск приложения...
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Установите Python 3.8+ с сайта python.org
    pause
    exit /b 1
)

REM Запускаем приложение
echo Запуск Photo Sorter...
python start.py

REM Если произошла ошибка, ждем ввода
if errorlevel 1 (
    echo.
    echo Произошла ошибка при запуске.
    pause
)
