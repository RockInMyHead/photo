"""
Photo Sorter for organizing photos by detected people
"""

import os
import shutil
from PyQt6.QtCore import QThread, pyqtSignal


class PhotoSorter(QThread):
    """Thread for sorting photos by people"""

    progress_updated = pyqtSignal(int, str)  # value, text
    sorting_finished = pyqtSignal(dict)  # sorted_groups

    def __init__(self):
        super().__init__()
        self.face_groups = {}
        self.output_directory = ""
        self.group_names = {}

    def sort_photos(self, face_groups, output_directory, group_names=None):
        """Start sorting photos by people"""
        self.face_groups = face_groups
        self.output_directory = output_directory
        self.group_names = group_names or {}
        self.start()

    def run(self):
        """Sort photos in background thread"""
        if not self.face_groups or not self.output_directory:
            self.sorting_finished.emit({})
            return

        sorted_groups = {}

        total_groups = len(self.face_groups)
        processed_groups = 0

        for group_id, photos in self.face_groups.items():
            if self.isInterruptionRequested():
                return

            # Create group directory
            group_name = self.group_names.get(group_id, f"Person_{group_id + 1}")
            group_dir = os.path.join(self.output_directory, group_name)

            try:
                os.makedirs(group_dir, exist_ok=True)

                sorted_groups[group_id] = []

                for photo_path in photos:
                    if self.isInterruptionRequested():
                        return

                    # Copy photo to group directory
                    filename = os.path.basename(photo_path)
                    new_path = os.path.join(group_dir, filename)

                    # Avoid overwriting files with same name
                    if os.path.exists(new_path):
                        name, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(new_path):
                            new_path = os.path.join(group_dir, f"{name}_{counter}{ext}")
                            counter += 1

                    try:
                        shutil.copy2(photo_path, new_path)
                        sorted_groups[group_id].append(new_path)
                    except Exception as e:
                        print(f"Error copying {photo_path}: {e}")

            except Exception as e:
                print(f"Error creating directory {group_dir}: {e}")

            processed_groups += 1
            progress = int((processed_groups / total_groups) * 100)
            self.progress_updated.emit(
                progress,
                f"Сортировка: {processed_groups}/{total_groups} групп"
            )

        self.sorting_finished.emit(sorted_groups)

    def get_group_statistics(self):
        """Get statistics about sorted groups"""
        if not self.face_groups:
            return {}

        stats = {}
        for group_id, photos in self.face_groups.items():
            group_name = self.group_names.get(group_id, f"Person_{group_id + 1}")
            stats[group_name] = {
                'photo_count': len(photos),
                'group_id': group_id
            }

        return stats

