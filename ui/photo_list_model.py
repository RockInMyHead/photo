"""
Photo List Model for displaying photos in QListView
"""

import os
from PyQt6.QtCore import QAbstractListModel, Qt
from PyQt6.QtGui import QPixmap, QIcon


class PhotoListModel(QAbstractListModel):
    """Model for displaying photos in a list view"""

    def __init__(self, photos=None):
        super().__init__()
        self.photos = photos or []

    def rowCount(self, parent=None):
        """Return number of photos"""
        return len(self.photos)

    def data(self, index, role):
        """Return data for given index and role"""
        if not index.isValid() or index.row() >= len(self.photos):
            return None

        photo_path = self.photos[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            # Return filename
            return os.path.basename(photo_path)

        elif role == Qt.ItemDataRole.ToolTipRole:
            # Return full path as tooltip
            return photo_path

        elif role == Qt.ItemDataRole.DecorationRole:
            # Return thumbnail
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                # Scale to thumbnail size
                thumbnail = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
                return QIcon(thumbnail)

        return None

    def update_photos(self, photos):
        """Update the list of photos"""
        self.beginResetModel()
        self.photos = photos
        self.endResetModel()

    def get_photo_path(self, index):
        """Get photo path for given index"""
        if 0 <= index < len(self.photos):
            return self.photos[index]
        return None

