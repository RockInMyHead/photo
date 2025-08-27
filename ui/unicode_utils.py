#!/usr/bin/env python3
"""
Unicode utilities for handling Russian/Unicode file paths with OpenCV
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageOps


def imread_unicode(filepath, flags=cv2.IMREAD_COLOR):
    """
    Safe imread function that handles Unicode/Russian paths
    
    Args:
        filepath: Path to image file (can contain Unicode characters)
        flags: OpenCV imread flags
        
    Returns:
        numpy.ndarray: Image array or None if failed
    """
    try:
        # Method 1: Try PIL first (handles Unicode better)
        with Image.open(filepath) as pil_image:
            # Convert PIL to OpenCV format
            if flags == cv2.IMREAD_GRAYSCALE:
                pil_image = pil_image.convert('L')
                cv_image = np.array(pil_image)
            else:
                # Handle EXIF orientation
                pil_image = ImageOps.exif_transpose(pil_image)
                pil_image = pil_image.convert('RGB')
                cv_image = np.array(pil_image)
                # Convert RGB to BGR for OpenCV
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
            
            return cv_image
            
    except Exception as e:
        print(f"PIL failed for {filepath}: {e}")
        
        try:
            # Method 2: Use numpy fromfile + cv2.imdecode
            with open(filepath, 'rb') as f:
                file_bytes = f.read()
            
            # Convert to numpy array
            np_array = np.frombuffer(file_bytes, np.uint8)
            
            # Decode image
            cv_image = cv2.imdecode(np_array, flags)
            return cv_image
            
        except Exception as e2:
            print(f"cv2.imdecode failed for {filepath}: {e2}")
            
            try:
                # Method 3: Copy to temp file with ASCII name
                import tempfile
                import shutil
                
                # Get file extension
                _, ext = os.path.splitext(filepath)
                
                # Create temp file
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # Copy file
                shutil.copy2(filepath, temp_path)
                
                # Read with OpenCV
                cv_image = cv2.imread(temp_path, flags)
                
                # Clean up
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                return cv_image
                
            except Exception as e3:
                print(f"Temp file method failed for {filepath}: {e3}")
                return None


def imwrite_unicode(filepath, img):
    """
    Safe imwrite function that handles Unicode/Russian paths
    
    Args:
        filepath: Output path (can contain Unicode characters)
        img: Image array to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Method 1: Use cv2.imencode + direct file write
        # Get file extension
        _, ext = os.path.splitext(filepath)
        if not ext:
            ext = '.jpg'
        
        # Encode image
        success, img_encoded = cv2.imencode(ext, img)
        if not success:
            return False
        
        # Write to file
        with open(filepath, 'wb') as f:
            f.write(img_encoded.tobytes())
        
        return True
        
    except Exception as e:
        print(f"Unicode imwrite failed for {filepath}: {e}")
        return False


def test_unicode_support():
    """Test if Unicode file paths work with OpenCV"""
    print("🔍 Тестирование поддержки Unicode путей...")
    
    # Test files with different characters
    test_cases = [
        "test_ascii.jpg",
        "тест_русский.jpg", 
        "测试_中文.jpg",
        "テスト_日本語.jpg"
    ]
    
    for test_file in test_cases:
        try:
            # Try standard cv2.imread
            img1 = cv2.imread(test_file)
            if img1 is not None:
                print(f"✅ cv2.imread работает: {test_file}")
            else:
                print(f"❌ cv2.imread не работает: {test_file}")
                
            # Try our Unicode-safe function
            img2 = imread_unicode(test_file)
            if img2 is not None:
                print(f"✅ imread_unicode работает: {test_file}")
            else:
                print(f"❌ imread_unicode не работает: {test_file}")
                
        except Exception as e:
            print(f"⚠️ Ошибка тестирования {test_file}: {e}")


if __name__ == "__main__":
    test_unicode_support()
