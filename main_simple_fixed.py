#!/usr/bin/env python3
"""
Photo Sorter Application - Simple Version (Fixed)
Uses OpenCV face detection without face-recognition library
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """Main application entry point"""
    # Enable high DPI scaling for better display on high-resolution screens
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Photo Sorter - Simple")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PhotoTools")

    # Import and create main window
    from ui.main_window_simple import MainWindow
    window = MainWindow()
    window.show()

    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


