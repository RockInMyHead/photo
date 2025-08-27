#!/usr/bin/env python3
"""
Photo Sorter Application Launcher
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from ui.main_window import MainWindow
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt

    def main():
        """Main application launcher"""
        # Enable high DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Photo Sorter")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("PhotoTools")

        # Create and show main window
        window = MainWindow()
        window.show()

        # Start event loop
        sys.exit(app.exec())

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("\nПожалуйста, установите необходимые зависимости:")
    print("pip install -r requirements.txt")
    print("\nНеобходимые компоненты:")
    print("- PyQt6")
    print("- opencv-python")
    print("- face-recognition")
    print("- numpy")
    print("- Pillow")
    sys.exit(1)

