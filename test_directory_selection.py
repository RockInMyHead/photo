#!/usr/bin/env python3
"""
Test script to verify directory selection works
"""

import sys
import os

def test_imports():
    """Test PyQt6 imports"""
    try:
        from PyQt6.QtWidgets import QApplication, QFileDialog
        print("✅ PyQt6 imports OK")
        return True
    except ImportError as e:
        print(f"❌ PyQt6 import failed: {e}")
        return False

def test_qfiledialog():
    """Test QFileDialog functionality"""
    try:
        app = QApplication(sys.argv)

        # Test without parent
        directory = QFileDialog.getExistingDirectory(
            None, "Test: Select Directory"
        )

        if directory:
            print(f"✅ QFileDialog works: {directory}")
            return True
        else:
            print("ℹ️ QFileDialog: User cancelled")
            return True

    except Exception as e:
        print(f"❌ QFileDialog failed: {e}")
        return False

def main():
    """Main test"""
    print("🔍 Testing Directory Selection")
    print("=" * 40)

    if not test_imports():
        return

    print("\n🗂️ Testing QFileDialog...")
    test_qfiledialog()

    print("\n✅ Directory selection test completed")
    print("\n💡 If QFileDialog doesn't work in the app, use:")
    print("   - Manual path input field")
    print("   - Enter path like: D:\\photos or C:\\Users\\username\\Pictures")

if __name__ == "__main__":
    main()


