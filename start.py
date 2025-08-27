#!/usr/bin/env python3
"""
Простой запуск Photo Sorter
"""

import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from ui.main_window_simplified import MainWindowSimplified
    
    def main():
        """Главная функция запуска"""
        # Включаем поддержку высокого DPI
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        # Создаем приложение
        app = QApplication(sys.argv)
        app.setApplicationName("Photo Sorter")
        app.setApplicationVersion("2.0.0")
        app.setOrganizationName("PhotoTools")
        
        # Создаем и показываем главное окно
        window = MainWindowSimplified()
        window.show()
        
        # Запускаем цикл событий
        sys.exit(app.exec())
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print("Ошибка импорта:", e)
    print("\nУбедитесь, что установлены все зависимости:")
    print("pip install -r requirements.txt")
    print("pip install insightface onnxruntime")
    input("Нажмите Enter для выхода...")
except Exception as e:
    print("Ошибка запуска:", e)
    input("Нажмите Enter для выхода...")
