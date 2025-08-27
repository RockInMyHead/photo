#!/usr/bin/env python3
"""
Direct launcher that bypasses command line issues
"""

import sys
import subprocess
import os

def main():
    print("🚀 Direct Launcher для Photo Sorter")
    print("=" * 50)

    # Show current Python executable
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")

    # Try to import PyQt6 first
    print("\n📦 Проверка PyQt6...")
    try:
        import PyQt6.QtWidgets
        print("✅ PyQt6 доступен")
    except ImportError as e:
        print(f"❌ PyQt6 недоступен: {e}")
        print("Устанавливаем PyQt6...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"])
        return

    # Launch the application directly
    print("\n🚀 Запуск приложения...")
    try:
        # Import and run directly
        from main_simple import main as app_main
        app_main()
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
