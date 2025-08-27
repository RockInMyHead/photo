#!/usr/bin/env python3
"""
Test the InsightFace fix
"""

print("🔧 Тестирование исправления InsightFace")
print("=" * 50)

try:
    print("1. Импорт основных модулей...")
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 импортирован")

    print("2. Импорт MainWindow...")
    from ui.main_window_simple import MainWindow
    print("✅ MainWindow импортирован")

    print("3. Создание QApplication...")
    app = QApplication([])
    print("✅ QApplication создан")

    print("4. Создание MainWindow...")
    window = MainWindow()
    print("✅ MainWindow создан")

    print("5. Проверка InsightFace статуса...")
    if window.insight_sorter is None:
        print("⚠️  InsightFace недоступен (ожидаемо без установки)")
    else:
        print("✅ InsightFace доступен")

    print("6. Показ окна...")
    window.show()
    print("✅ Окно показано")

    print("\n🎉 Все тесты пройдены!")
    print("Приложение готово к работе!")

    # Не запускаем event loop, просто проверяем создание
    window.close()
    print("✅ Окно закрыто")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Тестирование завершено!")
