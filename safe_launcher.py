#!/usr/bin/env python3
"""
Safe launcher that bypasses PowerShell command issues
"""

import subprocess
import sys
import os

def main():
    print("🚀 Safe Launcher для Photo Sorter")
    print("=" * 50)

    # First run diagnostics
    print("1. Запуск диагностики...")
    try:
        result = subprocess.run([sys.executable, "quick_diagnostic.py"],
                              capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("Ошибки диагностики:", result.stderr)
    except Exception as e:
        print(f"Ошибка диагностики: {e}")

    # Try to run the application
    print("\n2. Запуск приложения...")
    try:
        cmd = [sys.executable, "main_simple.py"]
        print(f"Команда: {' '.join(cmd)}")

        # Run with output visible
        result = subprocess.run(cmd)
        print(f"\nПриложение завершено с кодом: {result.returncode}")

    except Exception as e:
        print(f"Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
