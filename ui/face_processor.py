"""
Face Processor for detecting and recognizing faces in photos
"""

import os
import cv2
import face_recognition
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from collections import defaultdict
from .unicode_utils import imread_unicode


class FaceProcessor(QThread):
    """Thread for processing faces in photos"""

    progress_updated = pyqtSignal(int, str)  # value, text
    processing_finished = pyqtSignal(dict)  # face_groups

    def __init__(self):
        super().__init__()
        self.photos = []
        self.face_encodings = []
        self.photo_faces = {}  # photo_path -> list of face encodings
        self.face_groups = {}  # group_id -> list of photos
        self.group_names = {}  # group_id -> name

    def process_photos(self, photos):
        """Start processing photos for faces"""
        self.photos = photos
        self.start()

    def run(self):
        """Process photos for face detection and recognition"""
        if not self.photos:
            self.processing_finished.emit({})
            return

        self.photo_faces = {}
        all_encodings = []
        encoding_to_photo = {}  # encoding index -> photo_path

        total_photos = len(self.photos)
        processed_photos = 0

        # Process each photo for faces
        for photo_path in self.photos:
            if self.isInterruptionRequested():
                return

            try:
                # Load image with Unicode-safe reading
                image = imread_unicode(photo_path)
                if image is None:
                    print(f"Не удалось загрузить изображение: {photo_path}")
                    continue

                # Convert to RGB (face_recognition expects RGB)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Find faces in the image
                face_locations = face_recognition.face_locations(rgb_image)
                face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

                if face_encodings:
                    self.photo_faces[photo_path] = face_encodings
                    # Store encodings with their photo mapping
                    for encoding in face_encodings:
                        encoding_idx = len(all_encodings)
                        all_encodings.append(encoding)
                        encoding_to_photo[encoding_idx] = photo_path

            except Exception as e:
                print(f"Error processing {photo_path}: {e}")
                continue

            processed_photos += 1
            progress = int((processed_photos / total_photos) * 50)  # First 50% for detection
            self.progress_updated.emit(progress, f"Обнаружение лиц: {processed_photos}/{total_photos}")

        if not all_encodings:
            self.processing_finished.emit({})
            return

        # Group similar faces together
        self.face_groups = self.group_faces(all_encodings, encoding_to_photo)

        # Update progress for grouping phase
        self.progress_updated.emit(100, "Группировка завершена")
        self.processing_finished.emit(self.face_groups)

    def group_faces(self, encodings, encoding_to_photo, tolerance=0.6):
        """Group similar faces together using clustering"""
        face_groups = defaultdict(list)
        used_encodings = set()

        group_id = 0

        for i, encoding1 in enumerate(encodings):
            if i in used_encodings:
                continue

            # Start a new group
            face_groups[group_id] = []
            used_encodings.add(i)

            photo_path = encoding_to_photo[i]
            if photo_path not in face_groups[group_id]:
                face_groups[group_id].append(photo_path)

            # Find similar faces
            for j, encoding2 in enumerate(encodings):
                if j in used_encodings or j == i:
                    continue

                # Calculate face distance
                distance = face_recognition.face_distance([encoding1], encoding2)[0]

                if distance < tolerance:  # Similar face
                    used_encodings.add(j)
                    photo_path = encoding_to_photo[j]
                    if photo_path not in face_groups[group_id]:
                        face_groups[group_id].append(photo_path)

            group_id += 1

        return dict(face_groups)

    def get_face_count_for_photo(self, photo_path):
        """Get number of faces detected in a photo"""
        return len(self.photo_faces.get(photo_path, []))

    def assign_name_to_group(self, group_id, name):
        """Assign a name to a face group"""
        self.group_names[group_id] = name

    def get_group_name(self, group_id):
        """Get name for a face group"""
        return self.group_names.get(group_id, f"Человек {group_id + 1}")

