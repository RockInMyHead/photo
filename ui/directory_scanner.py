"""
Directory Scanner for finding and cataloging photos
"""

import os
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QFileSystemModel


class DirectoryScanner(QThread):
    """Thread for scanning directories for photos"""

    progress_updated = pyqtSignal(int, str)  # value, text
    scanning_finished = pyqtSignal(list)  # photos list

    def __init__(self):
        super().__init__()
        self.directory = ""
        self.photos = []
        self.supported_extensions = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif',
            '.gif', '.webp', '.raw', '.cr2', '.nef', '.arw'
        }

    def scan_directory(self, directory):
        """Start scanning directory for photos"""
        self.directory = directory
        self.photos = []
        self.start()

    def run(self):
        """Scan directory for photos in background thread"""
        self.photos = []
        total_files = 0

        # First pass: count total files for progress calculation
        for root, dirs, files in os.walk(self.directory):
            total_files += len([f for f in files
                              if os.path.splitext(f.lower())[1] in self.supported_extensions])

        if total_files == 0:
            self.scanning_finished.emit([])
            return

        processed_files = 0

        # Second pass: collect photos with optimizations
        for root, dirs, files in os.walk(self.directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if self.isInterruptionRequested():
                    return

                # Skip hidden files
                if file.startswith('.'):
                    continue

                file_ext = os.path.splitext(file.lower())[1]
                if file_ext in self.supported_extensions:
                    photo_path = os.path.join(root, file)

                    # Quick size check (skip files larger than 100MB)
                    try:
                        file_size = os.path.getsize(photo_path)
                        if file_size > 100 * 1024 * 1024:  # 100MB
                            continue
                        if file_size < 1024:  # Skip files smaller than 1KB
                            continue
                    except OSError:
                        continue

                    self.photos.append(photo_path)

                    processed_files += 1
                    progress = int((processed_files / max(total_files, 1)) * 100)

                    self.progress_updated.emit(
                        progress,
                        f"Найдено: {processed_files} фото"
                    )

        self.scanning_finished.emit(self.photos)


class PhotoListModel:
    """Model for displaying photos in a list view"""

    def __init__(self, photos=None):
        self.photos = photos or []

    def rowCount(self):
        """Return number of photos"""
        return len(self.photos)

    def data(self, index, role):
        """Return data for given index and role"""
        if not index.isValid() or index.row() >= len(self.photos):
            return None

        if role == 0:  # DisplayRole
            return os.path.basename(self.photos[index.row()])

        return None

    def update_photos(self, photos):
        """Update the list of photos"""
        self.photos = photos
