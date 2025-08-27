#!/usr/bin/env python3
"""
Простой скрипт для загрузки Photo Sorter на GitHub
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Выполнить команду и вернуть результат"""
    try:
        print(f"🔄 Выполняю: {' '.join(command)}")
        result = subprocess.run(
            command,
            cwd=cwd or os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.stdout:
            print(f"✅ Вывод: {result.stdout.strip()}")
        
        if result.stderr and "fatal" not in result.stderr.lower():
            print(f"⚠️ Предупреждения: {result.stderr.strip()}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Главная функция загрузки"""
    print("🚀 Загружаю Photo Sorter на GitHub...")
    print("=" * 60)
    
    # Проверяем Git
    if not run_command(["git", "--version"]):
        print("❌ Git не найден. Установите Git и добавьте в PATH")
        input("Нажмите Enter для выхода...")
        return
    
    # Инициализируем репозиторий если нужно
    if not Path(".git").exists():
        print("📁 Инициализирую git репозиторий...")
        if not run_command(["git", "init"]):
            print("❌ Не удалось инициализировать git")
            return
        
        # Настраиваем пользователя
        run_command(["git", "config", "user.name", "RockInMyHead"])
        run_command(["git", "config", "user.email", "rockinmyhead@example.com"])
    
    # Добавляем удаленный репозиторий
    print("🌐 Настраиваю удаленный репозиторий...")
    run_command(["git", "remote", "remove", "origin"])
    if not run_command(["git", "remote", "add", "origin", "https://github.com/RockInMyHead/photo.git"]):
        print("❌ Не удалось добавить удаленный репозиторий")
        return
    
    # Добавляем все файлы
    print("📂 Добавляю файлы в репозиторий...")
    if not run_command(["git", "add", "."]):
        print("❌ Не удалось добавить файлы")
        return
    
    # Создаем коммит
    commit_message = '''Photo Sorter - Автоматическая сортировка фотографий

✅ НОВЫЕ ВОЗМОЖНОСТИ:
• Полностью автоматизированный процесс сортировки
• Пакетная обработка нескольких папок
• Темная тема с высокой контрастностью
• Упрощенный интерфейс без лишних описаний
• Проводник для просмотра фотографий
• Система очередей для управления задачами

🎯 ОСНОВНЫЕ ФУНКЦИИ:
• Выбор папки → Автоматическая обработка
• Сканирование фотографий
• Распознавание лиц
• Группировка по людям
• Создание структурированных папок

🎨 ИНТЕРФЕЙС:
• Светлая и темная темы
• Настройки производительности
• Тест контрастности
• Современный дизайн

⚡ ПРОИЗВОДИТЕЛЬНОСТЬ:
• Многопоточная обработка
• Оптимизация памяти
• Быстрая навигация

🧹 ОЧИСТКА ПРОЕКТА:
• Удалены все тестовые файлы
• Убраны дублирующиеся скрипты
• Оставлен только рабочий функционал
• Чистая структура проекта'''
    
    print("💾 Создаю коммит...")
    if not run_command(["git", "commit", "-m", commit_message]):
        print("❌ Не удалось создать коммит")
        return
    
    # Проверяем текущую ветку
    print("🌿 Проверяю ветку...")
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    current_branch = result.stdout.strip() or "master"
    print(f"📌 Текущая ветка: {current_branch}")
    
    # Отправляем на GitHub
    print("🚀 Отправляю на GitHub...")
    if not run_command(["git", "push", "-u", "origin", current_branch]):
        print("⚠️ Пробую принудительную отправку...")
        if not run_command(["git", "push", "-u", "origin", current_branch, "--force"]):
            print("❌ Не удалось отправить на GitHub")
            return
    
    print("=" * 60)
    print("🎉 Проект успешно загружен на GitHub!")
    print(f"🌐 Репозиторий: https://github.com/RockInMyHead/photo")
    print("=" * 60)
    
    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
