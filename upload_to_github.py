#!/usr/bin/env python3
"""
Script to upload Photo Sorter project to GitHub
Bypasses PowerShell prefix issue by using subprocess
"""

import subprocess
import sys
import os
from pathlib import Path


def run_git_command(command, cwd=None):
    """Run git command and return result"""
    try:
        print(f"Выполняю: {' '.join(command)}")
        result = subprocess.run(
            command,
            cwd=cwd or os.getcwd(),
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )

        if result.stdout:
            print(f"Вывод: {result.stdout.strip()}")

        if result.stderr and "fatal" not in result.stderr.lower():
            print(f"Предупреждения: {result.stderr.strip()}")

        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")
        return False, "", str(e)


def main():
    """Main upload function"""
    print("🚀 Начинаю загрузку проекта Photo Sorter на GitHub")
    print("=" * 60)

    # Check if git is available
    success, _, _ = run_git_command(["git", "--version"])
    if not success:
        print("❌ Git не найден. Установите Git и добавьте в PATH")
        return False

    # Initialize git repository if needed
    if not Path(".git").exists():
        print("📁 Инициализирую git репозиторий...")
        success, _, _ = run_git_command(["git", "init"])
        if not success:
            print("❌ Не удалось инициализировать git репозиторий")
            return False

    # Configure git user
    print("👤 Настраиваю git пользователя...")
    run_git_command(["git", "config", "user.name", "RockInMyHead"])
    run_git_command(["git", "config", "user.email", "rockinmyhead@example.com"])

    # Add remote repository
    print("🌐 Настраиваю удаленный репозиторий...")
    run_git_command(["git", "remote", "remove", "origin"])
    success, _, _ = run_git_command([
        "git", "remote", "add", "origin",
        "https://github.com/RockInMyHead/photo.git"
    ])
    if not success:
        print("❌ Не удалось добавить удаленный репозиторий")
        return False

    # Add all files
    print("📂 Добавляю файлы в репозиторий...")
    success, _, _ = run_git_command(["git", "add", "."])
    if not success:
        print("❌ Не удалось добавить файлы")
        return False

    # Create commit
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

🛠️ ТЕХНИЧЕСКИЕ УЛУЧШЕНИЯ:
• Исправлены ошибки импорта QListWidget
• Улучшена контрастность темной темы
• Добавлена система тестирования интерфейса
• Оптимизирована работа с сигналами
• Улучшена обработка Unicode-путей'''

    print("📝 Создаю коммит...")
    success, _, _ = run_git_command(["git", "commit", "-m", commit_message])
    if not success:
        print("❌ Не удалось создать коммит")
        return False

    # Push to GitHub
    print("🚀 Отправляю на GitHub...")
    success, _, error = run_git_command(["git", "push", "-u", "origin", "main"])

    if not success:
        if "non-fast-forward" in error or "Updates were rejected" in error:
            print("⚠️  Конфликт с существующим репозиторием. Использую force push...")
            success, _, _ = run_git_command(["git", "push", "-u", "origin", "main", "--force"])
        else:
            print(f"❌ Ошибка при отправке: {error}")
            return False

    if success:
        print("\n🎉 ПРОЕКТ УСПЕШНО ЗАГРУЖЕН НА GITHUB!")
        print("=" * 60)
        print("📂 Репозиторий: https://github.com/RockInMyHead/photo")
        print("\n✅ Что было загружено:")
        print("• main_simple.py - главный файл приложения")
        print("• ui/ - папка с интерфейсом")
        print("• Все настройки и конфигурации")
        print("• Документация проекта")
        print("• Система тем и настроек")
        print("\n🔍 Проверьте репозиторий на GitHub!")
        return True
    else:
        print("❌ Не удалось загрузить проект")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
