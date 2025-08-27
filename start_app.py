#!/usr/bin/env python3
"""
Simple launcher for Photo Sorter that handles errors gracefully
"""

import sys
import os

def main():
    """Launch the Photo Sorter application"""
    print("🚀 Starting Photo Sorter Application...")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        return

    print(f"✅ Python version: {sys.version.split()[0]}")

    # Check if we're in the right directory
    if not os.path.exists('ui'):
        print("❌ Error: ui directory not found")
        print("Please run this script from the project root directory")
        input("Press Enter to exit...")
        return

    # Try to import required modules
    try:
        import PyQt6.QtWidgets
        print("✅ PyQt6 found")
    except ImportError as e:
        print(f"❌ PyQt6 not found: {e}")
        print("Please run: pip install PyQt6")
        input("Press Enter to exit...")
        return

    try:
        import cv2
        print("✅ OpenCV found")
    except ImportError as e:
        print(f"❌ OpenCV not found: {e}")
        print("Please run: pip install opencv-python")
        input("Press Enter to exit...")
        return

    try:
        import face_recognition
        print("✅ face-recognition found")
    except ImportError as e:
        print(f"❌ face-recognition not found: {e}")
        print("Please run: pip install face-recognition")
        input("Press Enter to exit...")
        return

    # Try to launch the main application
    try:
        print("🔄 Launching main application...")
        from ui.main_window import MainWindow
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Photo Sorter")
        app.setApplicationVersion("1.0.0")

        # Create and show main window
        window = MainWindow()
        window.show()

        print("✅ Application window created")

        # Start event loop
        sys.exit(app.exec())

    except Exception as e:
        print(f"❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

