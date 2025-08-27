#!/usr/bin/env python3
"""
Simple GUI test to check if PyQt6 is working properly
"""

import sys
import traceback

try:
    print("Testing PyQt6 imports...")
    from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
    from PyQt6.QtCore import Qt
    print("✅ PyQt6 imports successful")

    print("Testing OpenCV imports...")
    import cv2
    print("✅ OpenCV import successful")

    print("Testing numpy imports...")
    import numpy as np
    print("✅ NumPy import successful")

    print("Testing Pillow imports...")
    from PIL import Image
    print("✅ Pillow import successful")

    print("\nСоздание простого окна...")

    app = QApplication(sys.argv)

    # Create a simple window
    window = QWidget()
    window.setWindowTitle("Тест PyQt6")
    window.setGeometry(100, 100, 400, 200)

    layout = QVBoxLayout()

    label1 = QLabel("✅ PyQt6 работает!")
    label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label1)

    label2 = QLabel("Если вы видите это окно, значит всё в порядке")
    label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label2)

    window.setLayout(layout)
    window.show()

    print("✅ Окно создано и показано")
    print("Если окно не появилось, проблема с отображением PyQt6")

    sys.exit(app.exec())

except Exception as e:
    print(f"❌ Ошибка: {e}")
    traceback.print_exc()
    input("Нажмите Enter для выхода...")
