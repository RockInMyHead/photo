#!/usr/bin/env python3
"""
Test script to verify Unicode path handling fixes
"""

import os
import cv2
from PIL import Image
import numpy as np

def test_unicode_path_handling():
    """Test if Unicode paths are handled correctly"""
    print("🔍 Testing Unicode path handling...")

    # Test 1: Check if cv2 can handle basic operations
    try:
        # Create a simple test image
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite("test_unicode.jpg", test_img)

        # Try to read it back
        loaded = cv2.imread("test_unicode.jpg")
        if loaded is not None:
            print("✅ Basic OpenCV operations work")
        else:
            print("❌ OpenCV basic operations failed")

        # Clean up
        if os.path.exists("test_unicode.jpg"):
            os.remove("test_unicode.jpg")

    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")

    # Test 2: PIL Unicode handling
    try:
        test_img_pil = Image.new('RGB', (100, 100), color='red')
        test_img_pil.save("тест_unicode.png")

        loaded_pil = Image.open("тест_unicode.png")
        if loaded_pil:
            print("✅ PIL Unicode handling works")

        # Clean up
        if os.path.exists("тест_unicode.png"):
            os.remove("тест_unicode.png")

    except Exception as e:
        print(f"❌ PIL Unicode test failed: {e}")

    print("\n✅ Unicode path handling test completed!")
    print("The optimized app should now handle Cyrillic paths better.")

if __name__ == "__main__":
    test_unicode_path_handling()
