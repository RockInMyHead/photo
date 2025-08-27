#!/usr/bin/env python3
"""
Check Photo Sorter installation status
"""

import sys
import subprocess

def check_command(cmd, description):
    """Check if command works"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}")
            return False
    except:
        print(f"❌ {description}")
        return False

def check_import(module, description):
    """Check if module can be imported"""
    try:
        __import__(module)
        print(f"✅ {description}")
        return True
    except ImportError:
        print(f"❌ {description}")
        return False

def main():
    """Check installation status"""
    print("🔍 Проверка установки Photo Sorter")
    print("=" * 50)

    # Check Python
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info >= (3, 12):
        print("⚠️  Python 3.12 - возможны проблемы совместимости")
    elif sys.version_info >= (3, 8):
        print("✅ Python version compatible")
    else:
        print("❌ Python 3.8+ required")
        return

    print("\n📦 Проверка команд:")
    check_command("python --version", "Python доступен")
    check_command("pip --version", "pip доступен")

    print("\n📚 Проверка модулей:")
    modules = [
        ("PyQt6.QtWidgets", "PyQt6 (GUI)"),
        ("cv2", "OpenCV (компьютерное зрение)"),
        ("numpy", "NumPy (вычисления)"),
        ("PIL", "Pillow (изображения)"),
        ("face_recognition", "Face Recognition (распознавание лиц)")
    ]

    success_count = 0
    for module, description in modules:
        if check_import(module, description):
            success_count += 1

    print(f"\n📊 Результат: {success_count}/{len(modules)} модулей установлены")

    print("\n" + "=" * 50)

    if success_count == len(modules):
        print("🎉 Отлично! Все готово для запуска")
        print("\n🚀 Запустите приложение:")
        print("   python main.py")
        print("   или")
        print("   python run.py")

    elif success_count >= 3:
        print("⚠️  Основные компоненты установлены")
        print("Приложение может работать с ограниченной функциональностью")
        print("\n🚀 Попробуйте запустить:")
        print("   python main.py")

    else:
        print("❌ Недостаточно компонентов")
        print("\n🔧 Установите зависимости:")
        print("   python install_deps.py")
        print("   или")
        print("   pip install PyQt6 opencv-python numpy Pillow face-recognition")

    print("\n📖 Подробные инструкции: INSTALLATION_GUIDE.md")
    print("=" * 50)

if __name__ == "__main__":
    main()


