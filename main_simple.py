#!/usr/bin/env python3
"""
Photo Sorter Application - Simple Version (without face-recognition)
Uses OpenCV built-in face detection
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from ui.main_window_simplified import MainWindowSimplified as MainWindow

def main():
    """Main application entry point"""
    try:
        print("Запуск приложения...")
        # Enable high DPI scaling for better display on high-resolution screens
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Create application
        print("Создание QApplication...")
        app = QApplication(sys.argv)
        app.setApplicationName("Photo Sorter - Simple")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("PhotoTools")

        # Create and show main window
        print("Создание главного окна...")
        window = MainWindow()
        print("Показ главного окна...")
        window.show()

        print("Запуск цикла событий...")
        # Start event loop
        sys.exit(app.exec())
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()


