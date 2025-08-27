#!/usr/bin/env python3
"""Test script to check if Python and modules work"""

import sys
print(f"Python version: {sys.version}")

try:
    import PyQt6.QtWidgets
    print("✅ PyQt6 is available")
except ImportError as e:
    print(f"❌ PyQt6 error: {e}")

try:
    import cv2
    print("✅ OpenCV is available")
except ImportError as e:
    print(f"❌ OpenCV error: {e}")

try:
    import face_recognition
    print("✅ face-recognition is available")
except ImportError as e:
    print(f"❌ face-recognition error: {e}")

print("Test completed!")

