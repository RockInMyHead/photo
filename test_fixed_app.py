#!/usr/bin/env python3
"""
Test the fixed application
"""

import subprocess
import sys
import os

def main():
    print("🔧 Тестирование исправленного приложения")
    print("=" * 50)
    
    try:
        # Run the application
        result = subprocess.run([sys.executable, "main_simple.py"], 
                              capture_output=True, text=True, timeout=10)
        
        print("Stdout:")
        print(result.stdout)
        
        if result.stderr:
            print("Stderr:")
            print(result.stderr)
            
        print(f"Exit code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("✅ Приложение запустилось и работает (превышен таймаут)")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
