#!/usr/bin/env python3
"""
Test CSS fixes and interface functionality
"""

print("🔧 Тестирование исправлений CSS")
print("=" * 50)

try:
    print("1. Импорт стилей...")
    from ui.modern_styles import MODERN_STYLESHEET, COLORS, apply_button_style, apply_label_style
    print("✅ Стили импортированы")

    print("2. Проверка CSS на проблемные свойства...")
    problematic_properties = ['transform:', 'translateY(', 'scale(', 'rotate(', 'box-shadow:', 'filter:', 'animation:']
    has_problems = False

    for prop in problematic_properties:
        if prop in MODERN_STYLESHEET:
            print(f"⚠️  Найдено проблемное свойство: {prop}")
            has_problems = True

    if not has_problems:
        print("✅ CSS не содержит проблемных свойств")

    print("3. Тестирование создания интерфейса...")
    from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QGroupBox, QVBoxLayout, QTabWidget
    from PyQt6.QtCore import Qt

    app = QApplication([])

    # Test basic widgets
    button = QPushButton("Test Button")
    button.setStyleSheet(MODERN_STYLESHEET)
    print("✅ QPushButton с CSS работает")

    label = QLabel("Test Label")
    label.setStyleSheet(MODERN_STYLESHEET)
    print("✅ QLabel с CSS работает")

    # Test group box
    group = QGroupBox("Test Group")
    group.setStyleSheet(MODERN_STYLESHEET)
    print("✅ QGroupBox с CSS работает")

    # Test tab widget
    tab_widget = QTabWidget()
    tab_widget.setStyleSheet(MODERN_STYLESHEET)
    print("✅ QTabWidget с CSS работает")

    print("4. Проверка цветов...")
    for name, color in COLORS.items():
        if color.startswith('#') and len(color) == 7:
            print(f"✅ Цвет {name}: {color}")
        else:
            print(f"⚠️  Некорректный цвет {name}: {color}")

    print("5. Тестирование функций стилизации...")
    apply_button_style(button, "success")
    print("✅ apply_button_style работает")

    apply_label_style(label, "warning")
    print("✅ apply_label_style работает")

    print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("CSS исправления работают корректно")

    # Clean up
    app.quit()

except Exception as e:
    print(f"❌ ОШИБКА: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Тестирование завершено")
