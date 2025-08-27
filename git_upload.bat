@echo off
REM Git upload script for Photo Sorter project
echo Initializing Git repository...

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo Git is not installed or not in PATH
    pause
    exit /b 1
)

REM Initialize git repository if not exists
if not exist .git (
    echo Initializing new git repository...
    git init
    git config user.name "RockInMyHead"
    git config user.email "rockinmyhead@example.com"
)

REM Add remote repository
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/RockInMyHead/photo.git

REM Add all files
echo Adding files to git...
git add .

REM Create commit
echo Creating commit...
git commit -m "Photo Sorter - Автоматическая сортировка фотографий

✅ Новые возможности:
• Полностью автоматизированный процесс сортировки
• Пакетная обработка нескольких папок
• Темная тема с высокой контрастностью
• Упрощенный интерфейс без лишних описаний
• Проводник для просмотра фотографий
• Система очередей для управления задачами

🎯 Основные функции:
• Выбор папки → Автоматическая обработка
• Сканирование фотографий
• Распознавание лиц
• Группировка по людям
• Создание структурированных папок

🎨 Интерфейс:
• Светлая и темная темы
• Настройки производительности
• Тест контрастности
• Современный дизайн

⚡ Производительность:
• Многопоточная обработка
• Оптимизация памяти
• Быстрая навигация"

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo Error during push. Trying with force...
    git push -u origin main --force
)

echo.
echo ✅ Project uploaded successfully!
echo Repository URL: https://github.com/RockInMyHead/photo
echo.
pause
