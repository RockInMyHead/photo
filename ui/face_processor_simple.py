"""
Simplified Face Processor using OpenCV without face-recognition
"""

import os
import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from collections import defaultdict
from .unicode_utils import imread_unicode


class SimpleFaceProcessor(QThread):
    """Simple face processor using OpenCV built-in methods"""

    progress_updated = pyqtSignal(int, str)  # value, text
    processing_finished = pyqtSignal(dict)  # face_groups

    def __init__(self):
        super().__init__()
        self.photos = []
        self.photo_faces = {}  # photo_path -> list of face regions
        self.face_groups = {}  # group_id -> list of photos
        self.group_names = {}  # group_id -> name

    def process_photos(self, photos):
        """Start processing photos for faces"""
        self.photos = photos
        self.start()

    def run(self):
        """Process photos for face detection"""
        if not self.photos:
            self.processing_finished.emit({})
            return

        self.photo_faces = {}
        all_faces = []

        total_photos = len(self.photos)
        processed_photos = 0

        # Load face detection classifier
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        # Process each photo for faces
        for photo_path in self.photos:
            if self.isInterruptionRequested():
                return

            try:
                # Check if file exists and get size
                if not os.path.exists(photo_path):
                    continue

                file_size = os.path.getsize(photo_path)
                # Skip files larger than 50MB to prevent memory issues
                if file_size > 50 * 1024 * 1024:
                    continue

                # Load image with Unicode-safe reading
                image = imread_unicode(photo_path)
                if image is None:
                    print(f"Не удалось загрузить изображение: {photo_path}")
                    continue

                # Resize large images to prevent memory issues
                height, width = image.shape[:2]
                max_size = 1920  # Max dimension
                if max(height, width) > max_size:
                    scale = max_size / max(height, width)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Convert to grayscale for face detection
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces with optimized parameters
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=3,  # Reduced for speed
                    minSize=(20, 20),  # Smaller min size
                    maxSize=(300, 300)  # Limit max face size
                )

                if len(faces) > 0:
                    self.photo_faces[photo_path] = faces.tolist()
                    # Store face info for grouping
                    for face in faces:
                        all_faces.append({
                            'photo': photo_path,
                            'face': face,
                            'area': face[2] * face[3]  # width * height
                        })

            except Exception as e:
                print(f"Error processing {photo_path}: {e}")
                continue

            processed_photos += 1
            progress = int((processed_photos / total_photos) * 100)
            self.progress_updated.emit(progress, f"Обнаружение лиц: {processed_photos}/{total_photos}")

        # Group faces by size (simple grouping)
        if all_faces:
            self.face_groups = self.simple_group_faces(all_faces)

        self.processing_finished.emit(self.face_groups)

    def simple_group_faces(self, faces):
        """Simple grouping based on face size"""
        # Sort faces by size
        faces_sorted = sorted(faces, key=lambda x: x['area'], reverse=True)

        groups = defaultdict(list)
        group_id = 0

        for face_info in faces_sorted:
            photo_path = face_info['photo']
            if photo_path not in [p for group in groups.values() for p in group]:
                groups[group_id] = [photo_path]
                group_id += 1

        return dict(groups)

    def get_face_count_for_photo(self, photo_path):
        """Get number of faces detected in a photo"""
        return len(self.photo_faces.get(photo_path, []))

    def assign_name_to_group(self, group_id, name):
        """Assign a name to a face group"""
        self.group_names[group_id] = name

    def get_group_name(self, group_id):
        """Get name for a face group"""
        return self.group_names.get(group_id, f"Группа {group_id + 1}")
