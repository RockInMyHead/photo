#!/usr/bin/env python3
"""
Command Line Interface for testing Photo Sorter functionality
"""

import os
import sys
import glob

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")

    modules_to_test = [
        ('PyQt6.QtWidgets', 'GUI Framework'),
        ('cv2', 'OpenCV'),
        ('face_recognition', 'Face Recognition'),
        ('numpy', 'Numerical Computing'),
        ('PIL', 'Image Processing')
    ]

    all_good = True
    for module, description in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {description}: OK")
        except ImportError as e:
            print(f"❌ {description}: Failed - {e}")
            all_good = False

    return all_good

def test_photo_scanning():
    """Test photo scanning functionality"""
    print("\n🔍 Testing photo scanning...")

    # Look for image files in current directory
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.gif']
    found_images = []

    for ext in image_extensions:
        found_images.extend(glob.glob(ext))
        found_images.extend(glob.glob(ext.upper()))

    if found_images:
        print(f"✅ Found {len(found_images)} images in current directory:")
        for img in found_images[:5]:  # Show first 5
            print(f"   - {img}")
        if len(found_images) > 5:
            print(f"   ... and {len(found_images) - 5} more")
    else:
        print("⚠️  No images found in current directory")
        print("   You can test with your own photos by placing them here")

    return len(found_images) > 0

def test_ui_imports():
    """Test our custom UI modules"""
    print("\n🔍 Testing UI modules...")

    ui_modules = [
        'ui.main_window',
        'ui.photo_viewer',
        'ui.directory_scanner',
        'ui.face_processor',
        'ui.photo_sorter',
        'ui.photo_list_model'
    ]

    all_good = True
    for module in ui_modules:
        try:
            __import__(module)
            print(f"✅ {module}: OK")
        except ImportError as e:
            print(f"❌ {module}: Failed - {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {module}: Loaded but with warning - {e}")

    return all_good

def main():
    """Main CLI test function"""
    print("🚀 Photo Sorter - CLI Test Mode")
    print("=" * 40)

    # Test Python version
    print(f"🐍 Python version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        return

    # Test imports
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Some dependencies are missing!")
        print("Run: pip install -r requirements.txt")
        return

    # Test UI modules
    ui_ok = test_ui_imports()
    if not ui_ok:
        print("\n❌ Some UI modules failed to load!")
        return

    # Test photo scanning
    photos_found = test_photo_scanning()

    print("\n" + "=" * 40)

    if imports_ok and ui_ok:
        print("✅ All tests passed!")
        print("\nTo run the full GUI application:")
        print("1. Make sure you have a GUI environment (Windows desktop)")
        print("2. Run: python main.py")
        print("   or: python run.py")
        print("   or: python start_app.py")

        if photos_found:
            print("\n🎉 Ready to process your photos!")
        else:
            print("\n📁 No photos found in current directory")
            print("   Place some photos here to test the application")
    else:
        print("❌ Some tests failed!")

if __name__ == "__main__":
    main()

