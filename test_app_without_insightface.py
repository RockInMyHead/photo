#!/usr/bin/env python3
"""
Test the app without InsightFace to verify it works
"""

print("🔧 Тестирование приложения без InsightFace")
print("=" * 50)

try:
    print("1. Импорт PyQt6...")
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 работает")

    print("2. Создание QApplication...")
    app = QApplication([])
    print("✅ QApplication создан")

    print("3. Тестирование UI модулей...")
    
    # Test individual components
    from ui.photo_viewer import PhotoViewer
    print("✅ PhotoViewer импортирован")
    
    from ui.directory_scanner import DirectoryScanner
    print("✅ DirectoryScanner импортирован")
    
    from ui.face_processor_simple import SimpleFaceProcessor
    print("✅ SimpleFaceProcessor импортирован")
    
    from ui.photo_sorter import PhotoSorter
    print("✅ PhotoSorter импортирован")
    
    print("4. Тестирование InsightFaceSorter...")
    try:
        from ui.insight_sorter import InsightFaceSorter
        sorter = InsightFaceSorter()
        print("✅ InsightFaceSorter доступен")
    except Exception as e:
        print(f"⚠️ InsightFaceSorter недоступен: {e}")
        print("Это нормально без установки зависимостей")

    print("5. Создание MainWindow...")
    from ui.main_window_simple import MainWindow
    window = MainWindow()
    print("✅ MainWindow создан успешно")

    print("6. Проверка статуса InsightFace в UI...")
    if hasattr(window, 'insight_sorter') and window.insight_sorter is None:
        print("✅ InsightFace корректно отключен в UI")
    elif hasattr(window, 'insight_sorter') and window.insight_sorter is not None:
        print("✅ InsightFace доступен в UI")
    else:
        print("⚠️ Неопределенный статус InsightFace")

    print("7. Показ окна...")
    window.show()
    print("✅ Окно показано")

    print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("Приложение готово к использованию")
    
    # Clean up
    window.close()
    app.quit()

except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Тестирование завершено")
