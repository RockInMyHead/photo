#!/usr/bin/env python3
"""
Diagnostic script that writes results to file
"""

import sys
import os

def write_result(message):
    """Write message to both console and file"""
    print(message)
    with open('diagnostic_log.txt', 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def main():
    """Run diagnostics and write to file"""
    # Clear previous log
    with open('diagnostic_log.txt', 'w', encoding='utf-8') as f:
        f.write("Photo Sorter Diagnostic Log\n")
        f.write("=" * 40 + "\n")

    write_result("🚀 Starting Photo Sorter Diagnostics...")

    # Check Python version
    write_result(f"🐍 Python version: {sys.version.split()[0]}")

    if sys.version_info < (3, 8):
        write_result("❌ Python 3.8+ required!")
        return

    # Test basic imports
    write_result("\n🔍 Testing basic modules...")

    basic_modules = [
        'sys', 'os', 'glob'
    ]

    for module in basic_modules:
        try:
            __import__(module)
            write_result(f"✅ {module}: OK")
        except ImportError as e:
            write_result(f"❌ {module}: Failed - {e}")

    # Test PyQt6
    try:
        import PyQt6.QtWidgets
        write_result("✅ PyQt6: OK")
    except ImportError as e:
        write_result(f"❌ PyQt6: Failed - {e}")

    # Test OpenCV
    try:
        import cv2
        write_result("✅ OpenCV: OK")
    except ImportError as e:
        write_result(f"❌ OpenCV: Failed - {e}")

    # Test face recognition
    try:
        import face_recognition
        write_result("✅ face-recognition: OK")
    except ImportError as e:
        write_result(f"❌ face-recognition: Failed - {e}")

    # Test UI modules
    write_result("\n🔍 Testing UI modules...")

    ui_modules = [
        'ui.main_window',
        'ui.photo_viewer',
        'ui.directory_scanner',
        'ui.face_processor',
        'ui.photo_sorter',
        'ui.photo_list_model'
    ]

    for module in ui_modules:
        try:
            __import__(module)
            write_result(f"✅ {module}: OK")
        except ImportError as e:
            write_result(f"❌ {module}: Failed - {e}")
        except Exception as e:
            write_result(f"⚠️  {module}: Warning - {e}")

    write_result("\n📁 Checking files...")
    write_result(f"Current directory: {os.getcwd()}")

    required_files = ['main.py', 'run.py', 'requirements.txt', 'ui/__init__.py']
    for file in required_files:
        if os.path.exists(file):
            write_result(f"✅ {file}: Found")
        else:
            write_result(f"❌ {file}: Missing")

    write_result("\n" + "=" * 40)
    write_result("✅ Diagnostics completed!")
    write_result("Check diagnostic_log.txt for results")
    write_result("\nTo run the application:")
    write_result("1. python main.py")
    write_result("2. python run.py")
    write_result("3. python start_app.py")

if __name__ == "__main__":
    main()

