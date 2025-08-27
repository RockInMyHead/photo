#!/usr/bin/env python3
"""
Launch helper - creates a simple GUI window with instructions
"""

import sys
import os

# Try to create a simple GUI message
try:
    from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget
    from PyQt6.QtCore import Qt

    def show_message():
        """Show a message box with instructions"""
        app = QApplication(sys.argv)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Photo Sorter - Готово к запуску!")
        msg.setText("Приложение Photo Sorter успешно создано!\n\n"
                   "Для запуска:\n"
                   "1. Откройте командную строку\n"
                   "2. Перейдите в папку: cd D:\\photo\n"
                   "3. Запустите: python main.py\n\n"
                   "Или просто запустите start_app.bat")

        msg.setDetailedText(
            "Возможности:\n"
            "• Сканирование папок с фотографиями\n"
            "• Распознавание лиц\n"
            "• Сортировка по людям\n"
            "• Просмотр и управление фото\n\n"
            "Поддерживаемые форматы:\n"
            "JPG, PNG, BMP, TIFF, GIF, WebP, RAW"
        )

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    if __name__ == "__main__":
        show_message()

except ImportError:
    # Fallback to console message
    print("=" * 60)
    print("PHOTO SORTER - ГОТОВ К ЗАПУСКУ!")
    print("=" * 60)
    print()
    print("Приложение успешно создано в папке: D:\\photo")
    print()
    print("Для запуска выполните:")
    print("1. Откройте командную строку")
    print("2. cd D:\\photo")
    print("3. python main.py")
    print()
    print("Или запустите файл start_app.bat двойным щелчком")
    print()
    print("Возможности:")
    print("• Сканирование фотографий")
    print("• Распознавание лиц")
    print("• Сортировка по людям")
    print("• Просмотр и управление")
    print()
    print("Поддерживаемые форматы: JPG, PNG, BMP, TIFF, GIF, WebP, RAW")
    print("=" * 60)
    input("Нажмите Enter для выхода...")

