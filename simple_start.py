#!/usr/bin/env python3
"""
Simple startup script that avoids command line issues
"""

print("🚀 Photo Sorter - простой запуск")
print("=" * 40)

try:
    print("Импорт PyQt6...")
    from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
    from PyQt6.QtCore import Qt

    print("Импорт модулей приложения...")
    from ui.main_window_simple import MainWindow

    print("Создание приложения...")
    app = QApplication([])

    print("Создание главного окна...")
    window = MainWindow()

    print("Показ окна...")
    window.show()

    print("✅ Приложение запущено! Закройте это окно командной строки.")
    print("Если окно приложения не появилось, проверьте панель задач.")

    app.exec()

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Установите недостающие модули:")
    print("pip install PyQt6 opencv-python numpy Pillow")
    input("Нажмите Enter для выхода...")

except Exception as e:
    print(f"❌ Ошибка запуска: {e}")
    import traceback
    traceback.print_exc()
    input("Нажмите Enter для выхода...")
