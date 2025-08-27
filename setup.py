#!/usr/bin/env python3
"""
Setup script for Photo Sorter Application
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install Python dependencies"""
    print("Установка зависимостей...")

    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        print("✅ Зависимости успешно установлены!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка установки зависимостей: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        print(f"Текущая версия: {sys.version}")
        return False

    print(f"✅ Python версия: {sys.version}")
    return True

def main():
    """Main setup function"""
    print("🚀 Настройка Photo Sorter")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    print("\n🎉 Настройка завершена!")
    print("\nДля запуска приложения выполните:")
    print("python run.py")
    print("или")
    print("python main.py")

if __name__ == "__main__":
    main()

