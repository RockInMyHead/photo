#!/usr/bin/env python3
"""
Photo Sorting Application - Main Entry Point
A desktop application for sorting photos by people using face recognition
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow

def main():
    """Main application entry point"""
    # Enable high DPI scaling for better display on high-resolution screens
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

