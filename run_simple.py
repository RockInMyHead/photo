#!/usr/bin/env python3
"""
Photo Sorter Application - Simple Version Launcher
Uses OpenCV face detection without face-recognition library
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """Launch the simple version of Photo Sorter"""
    print("🚀 Starting Photo Sorter - Simple Version")
    print("Uses OpenCV face detection (no face-recognition library needed)")
    print("=" * 60)

    try:
        from ui.main_window_simple import MainWindow
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt

        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Photo Sorter - Simple")
        app.setApplicationVersion("1.0.0")

        # Create and show main window
        window = MainWindow()
        window.show()

        print("✅ Application started successfully!")
        print("Close this console window to exit the application.")

        # Start event loop
        sys.exit(app.exec())

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease make sure you have installed:")
        print("- PyQt6 (GUI framework)")
        print("- OpenCV (computer vision)")
        print("- NumPy (numerical computing)")
        print("- Pillow (image processing)")
        print("\nRun: pip install PyQt6 opencv-python numpy Pillow")
        input("Press Enter to exit...")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()


