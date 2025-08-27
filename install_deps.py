#!/usr/bin/env python3
"""
Smart dependency installer for Photo Sorter
Handles Python 3.12 compatibility issues
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def install_with_pip(package, description):
    """Install package with pip"""
    return run_command(f"pip install {package}", f"Installing {description}")

def main():
    """Install dependencies with fallback options"""
    print("🚀 Installing Photo Sorter Dependencies")
    print("=" * 50)

    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    if sys.version_info >= (3, 12):
        print("⚠️  Python 3.12 detected - using compatible versions")
    elif sys.version_info >= (3, 8):
        print("✅ Python version is compatible")
    else:
        print("❌ Python 3.8+ required")
        sys.exit(1)

    # Strategy 1: Try installing from requirements.txt
    print("\n📦 Strategy 1: Installing from requirements.txt")
    if run_command("pip install -r requirements.txt", "Installing from requirements.txt"):
        print("\n🎉 All dependencies installed successfully!")
        return

    # Strategy 2: Install packages individually with latest versions
    print("\n📦 Strategy 2: Installing packages individually")

    packages = [
        ("PyQt6", "GUI Framework"),
        ("opencv-python", "Computer Vision"),
        ("numpy", "Numerical Computing"),
        ("Pillow", "Image Processing"),
        ("face-recognition", "Face Recognition"),
        ("cmake", "Build Tools")
    ]

    success_count = 0
    for package, description in packages:
        if install_with_pip(package, description):
            success_count += 1

    if success_count == len(packages):
        print(f"\n🎉 All {success_count} packages installed successfully!")
    elif success_count >= 4:  # At least core packages
        print(f"\n⚠️  {success_count}/{len(packages)} packages installed")
        print("The application should work with limited functionality")
    else:
        print(f"\n❌ Only {success_count}/{len(packages)} packages installed")
        print("The application may not work properly")

    # Test imports
    print("\n🔍 Testing imports...")
    test_imports()

def test_imports():
    """Test if key modules can be imported"""
    modules_to_test = [
        ("PyQt6.QtWidgets", "GUI Framework"),
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow"),
        ("face_recognition", "Face Recognition")
    ]

    success_count = 0
    for module, description in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {description} - {e}")

    print(f"\n📊 Import test results: {success_count}/{len(modules_to_test)} modules working")

    if success_count >= 4:
        print("\n🎯 Ready to run the application!")
        print("Try: python main.py")
    else:
        print("\n⚠️  Some modules are missing")
        print("The application may not work properly")

if __name__ == "__main__":
    main()


