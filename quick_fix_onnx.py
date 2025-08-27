#!/usr/bin/env python3
"""
Quick fix for ONNXRuntime issue
"""

import subprocess
import sys

def main():
    print("🔧 Быстрое исправление ONNXRuntime")
    print("=" * 40)
    
    print("Попытка установки ONNXRuntime...")
    
    try:
        # Try different installation methods
        commands = [
            [sys.executable, "-m", "pip", "install", "onnxruntime"],
            [sys.executable, "-m", "pip", "install", "onnxruntime-cpu"],
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"\nМетод {i}: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Метод {i} успешен!")
                break
            else:
                print(f"❌ Метод {i} неудачен: {result.stderr[:100]}...")
        else:
            print("❌ Все методы неудачны")
    
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Test import
    print("\nПроверка импорта...")
    try:
        import onnxruntime
        print("✅ ONNXRuntime работает!")
    except ImportError:
        print("❌ ONNXRuntime недоступен")
    
    # Now test the app
    print("\nПроверка приложения...")
    try:
        from ui.main_window_simple import MainWindow
        print("✅ MainWindow импортируется")
    except Exception as e:
        print(f"❌ Ошибка MainWindow: {e}")

if __name__ == "__main__":
    main()
