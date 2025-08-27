"""
Photo Viewer Widget for displaying images
"""

from PyQt6.QtWidgets import QLabel, QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
import os


class PhotoViewer(QWidget):
    """Widget for viewing photos with zoom and pan capabilities"""

    def __init__(self):
        super().__init__()
        self.current_pixmap = None
        self.scale_factor = 1.0
        self.setup_ui()

    def setup_ui(self):
        """Setup the photo viewer interface"""
        layout = QVBoxLayout(self)

        # Scroll area for large images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.image_label)

        layout.addWidget(self.scroll_area)

        # Enable mouse wheel for zooming
        self.scroll_area.setMouseTracking(True)
        self.scroll_area.wheelEvent = self.wheel_event

    def load_photo(self, photo_path):
        """Load and display a photo with Unicode support"""
        if not os.path.exists(photo_path):
            self.image_label.setText("Файл не найден")
            return

        try:
            # Try QPixmap first (usually works well with Unicode)
            pixmap = QPixmap(photo_path)
            if pixmap.isNull():
                # Fallback: use PIL for better Unicode support
                from PIL import Image, ImageOps
                import tempfile
                import shutil
                
                try:
                    # Create temporary file with ASCII name
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        temp_path = temp_file.name
                    
                    # Use PIL to handle Unicode and convert
                    with Image.open(photo_path) as pil_image:
                        pil_image = ImageOps.exif_transpose(pil_image)
                        pil_image.save(temp_path, 'JPEG', quality=95)
                    
                    # Load with QPixmap
                    pixmap = QPixmap(temp_path)
                    
                    # Clean up
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                        
                except Exception as pil_error:
                    print(f"PIL fallback failed: {pil_error}")
                    self.image_label.setText("Не удалось загрузить изображение")
                    return

            self.current_pixmap = pixmap
            self.scale_factor = 1.0
            self.update_display()

        except Exception as e:
            print(f"Ошибка загрузки {photo_path}: {e}")
            self.image_label.setText(f"Ошибка загрузки: {str(e)}")

    def update_display(self):
        """Update the displayed image with current scale"""
        if self.current_pixmap is None:
            return

        # Scale the pixmap
        scaled_pixmap = self.current_pixmap.scaled(
            self.current_pixmap.size() * self.scale_factor,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.adjustSize()

    def wheel_event(self, event):
        """Handle mouse wheel for zooming"""
        if self.current_pixmap is None:
            return

        # Calculate zoom factor based on wheel delta
        zoom_factor = 1.1 if event.angleDelta().y() > 0 else 0.9

        # Limit zoom levels
        new_scale = self.scale_factor * zoom_factor
        if 0.1 <= new_scale <= 5.0:
            self.scale_factor = new_scale
            self.update_display()

    def zoom_in(self):
        """Zoom in on the image"""
        if self.current_pixmap and self.scale_factor < 5.0:
            self.scale_factor *= 1.2
            self.update_display()

    def zoom_out(self):
        """Zoom out of the image"""
        if self.current_pixmap and self.scale_factor > 0.1:
            self.scale_factor *= 0.8
            self.update_display()

    def reset_zoom(self):
        """Reset zoom to 100%"""
        if self.current_pixmap:
            self.scale_factor = 1.0
            self.update_display()

    def clear(self):
        """Clear the current image"""
        self.current_pixmap = None
        self.scale_factor = 1.0
        self.image_label.clear()
        self.image_label.setText("Выберите изображение для просмотра")

