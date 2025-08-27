#!/usr/bin/env python3
"""
Direct test of the application
"""

print("🔧 Прямое тестирование приложения")
print("=" * 50)

try:
    print("1. Импорт PyQt6...")
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    print("✅ PyQt6 импортирован")

    print("2. Импорт main_simple...")
    import main_simple
    print("✅ main_simple импортирован")

    print("3. Создание QApplication...")
    app = QApplication([])
    print("✅ QApplication создан")

    print("4. Импорт MainWindow...")
    from ui.main_window_simple import MainWindow
    print("✅ MainWindow импортирован")

    print("5. Создание MainWindow...")
    window = MainWindow()
    print("✅ MainWindow создан")

    print("6. Показ окна...")
    window.show()
    print("✅ Окно показано")

    print("🎉 Все компоненты работают!")
    print("Если окно не появилось, проблема в отображении")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
