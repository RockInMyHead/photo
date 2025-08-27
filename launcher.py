#!/usr/bin/env python3
"""
Launcher script to properly start the Photo Sorter application
"""

import sys
import subprocess
import os

def main():
    try:
        print("Запуск Photo Sorter через launcher...")
        print(f"Python path: {sys.executable}")
        print(f"Current directory: {os.getcwd()}")

        # Try to run the main application
        cmd = [sys.executable, "main_simple.py"]
        print(f"Executing: {' '.join(cmd)}")

        result = subprocess.run(cmd, cwd=os.getcwd())
        print(f"Exit code: {result.returncode}")

    except Exception as e:
        print(f"Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
