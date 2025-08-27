#!/usr/bin/env python3
"""
Quick diagnostic script for Photo Sorter white screen issue
"""

import sys
import os

print("🔍 Быстрая диагностика Photo Sorter")
print("=" * 50)

# Check Python version
print(f"🐍 Python: {sys.version}")

# Test basic imports
print("\n📦 Проверка зависимостей:")
modules = [
    ('PyQt6.QtWidgets', 'PyQt6 (GUI)'),
    ('cv2', 'OpenCV'),
    ('numpy', 'NumPy'),
    ('PIL', 'Pillow')
]

working_modules = 0
for module_name, description in modules:
    try:
        __import__(module_name)
        print(f"✅ {description}: OK")
        working_modules += 1
    except ImportError as e:
        print(f"❌ {description}: НЕТ - {e}")
    except Exception as e:
        print(f"⚠️  {description}: ОШИБКА - {e}")

print(f"\n📊 Результат: {working_modules}/{len(modules)} модулей работают")

# Check if we can create a simple GUI
print("\n🖼️ Проверка создания окна:")
try:
    from PyQt6.QtWidgets import QApplication, QWidget, QLabel
    from PyQt6.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Create a simple test window
    window = QWidget()
    window.setWindowTitle("Тест")
    window.setGeometry(100, 100, 300, 100)

    label = QLabel("Если вы видите это окно - PyQt6 работает!")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    from PyQt6.QtWidgets import QVBoxLayout
    layout = QVBoxLayout()
    layout.addWidget(label)
    window.setLayout(layout)

    window.show()
    print("✅ Тестовое окно создано успешно")

    # Clean up
    window.close()
    if app:
        app.processEvents()

except Exception as e:
    print(f"❌ Ошибка создания окна: {e}")
    import traceback
    traceback.print_exc()

print("\n💡 Рекомендации:")
if working_modules < 3:
    print("🔧 Установите недостающие зависимости:")
    print("   pip install PyQt6 opencv-python numpy Pillow")
else:
    print("✅ Основные зависимости установлены")
    print("🚀 Попробуйте запустить: python main_simple.py")

print("\nДля детальной диагностики запустите: python diagnostic.py")
print("=" * 50)
