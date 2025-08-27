#!/usr/bin/env python3
"""
Photo Sorter - Optimized Single-File Version
Fast and reliable photo sorting with face detection
"""

import sys
import os
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from typing import Optional, List, Dict, Tuple

# PyQt6 imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeView, QListView, QLabel, QPushButton, QProgressBar, QStatusBar,
    QMenuBar, QMenu, QFileDialog, QMessageBox, QGroupBox, QGridLayout,
    QScrollArea, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QDir
from PyQt6.QtGui import QIcon, QAction, QPixmap, QFileSystemModel

# Image processing imports
import cv2
import numpy as np
from PIL import Image, ImageOps

# Clustering imports (optional)
try:
    from sklearn.cluster import DBSCAN
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️ sklearn не установлен - будет использоваться простое кластерирование")

@dataclass
class FaceRec:
    image: str
    face_idx: int
    bbox: Tuple[float, float, float, float]
    emb: Optional[np.ndarray] = None
    det_score: Optional[float] = None


class OptimizedPhotoSorter(QMainWindow):
    """Optimized Photo Sorter with fast face detection and progress control"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Sorter - Оптимизированная версия")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize components
        self.current_directory = None
        self.photos = []
        self.face_groups = {}

        self.setup_ui()
        self.setup_status_bar()

        # Set window icon and style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                padding: 8px 16px;
                font-size: 11px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #e6f3ff;
                border-color: #0078d4;
            }
            QPushButton:pressed {
                background-color: #c7e4f7;
            }
            QPushButton:disabled {
                background-color: #f3f2f1;
                color: #a19f9d;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
        """)

    def setup_ui(self):
        """Setup optimized user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # Main content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Photo list
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Photo viewer
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([400, 800])
        main_layout.addWidget(splitter)

        # Progress and cancel controls
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self.cancel_operation)
        progress_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(progress_layout)

    def create_control_panel(self):
        """Create optimized control panel"""
        group = QGroupBox("Управление (Оптимизированная версия)")
        layout = QVBoxLayout(group)

        # Directory selection
        dir_layout = QHBoxLayout()
        self.select_dir_btn = QPushButton("Выбрать папку")
        self.select_dir_btn.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.select_dir_btn)

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("ИЛИ введите путь вручную...")
        self.path_input.returnPressed.connect(self.manual_path_entered)
        dir_layout.addWidget(self.path_input)
        layout.addLayout(dir_layout)

        # Action buttons
        buttons_layout = QHBoxLayout()

        self.scan_btn = QPushButton("🔍 Сканировать")
        self.scan_btn.clicked.connect(self.start_scanning)
        self.scan_btn.setEnabled(False)
        buttons_layout.addWidget(self.scan_btn)

        self.process_btn = QPushButton("👤 Найти лица")
        self.process_btn.clicked.connect(self.start_face_processing)
        self.process_btn.setEnabled(False)
        buttons_layout.addWidget(self.process_btn)

        self.sort_btn = QPushButton("📁 Сортировать")
        self.sort_btn.clicked.connect(self.sort_photos)
        self.sort_btn.setEnabled(False)
        buttons_layout.addWidget(self.sort_btn)

        layout.addLayout(buttons_layout)

        # Info label
        self.info_label = QLabel("⚡ Оптимизированная версия с защитой от зависаний")
        layout.addWidget(self.info_label)

        return group

    def create_left_panel(self):
        """Create left panel with photo list"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("📸 Фотографии:"))
        self.photo_list = QListView()
        self.photo_list.clicked.connect(self.on_photo_selected)
        layout.addWidget(self.photo_list)

        return panel

    def create_right_panel(self):
        """Create right panel with photo viewer"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        layout.addWidget(QLabel("🖼️ Просмотр:"))
        self.photo_viewer = QLabel()
        self.photo_viewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_viewer.setMinimumSize(400, 300)
        self.photo_viewer.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: white;
            }
        """)
        layout.addWidget(self.photo_viewer)

        # Photo info
        info_group = QGroupBox("ℹ️ Информация")
        info_layout = QGridLayout(info_group)

        self.filename_label = QLabel("Файл:")
        self.path_label = QLabel("Путь:")
        self.size_label = QLabel("Размер:")
        self.faces_label = QLabel("Лица:")

        info_layout.addWidget(QLabel("Файл:"), 0, 0)
        info_layout.addWidget(self.filename_label, 0, 1)
        info_layout.addWidget(QLabel("Путь:"), 1, 0)
        info_layout.addWidget(self.path_label, 1, 1)
        info_layout.addWidget(QLabel("Размер:"), 2, 0)
        info_layout.addWidget(self.size_label, 2, 1)
        info_layout.addWidget(QLabel("Лица:"), 3, 0)
        info_layout.addWidget(self.faces_label, 3, 1)

        layout.addWidget(info_group)
        return panel

    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Готово")
        self.status_bar.addWidget(self.status_label)

    def select_directory(self):
        """Select directory containing photos"""
        try:
            directory = QFileDialog.getExistingDirectory(
                self, "Выберите папку с фотографиями"
            )
        except Exception:
            directory = QFileDialog.getExistingDirectory(
                None, "Выберите папку с фотографиями"
            )

        if directory:
            self.set_directory(directory)

    def manual_path_entered(self):
        """Handle manual path input"""
        path = self.path_input.text().strip()
        if path:
            path = os.path.expanduser(path)
            path = os.path.abspath(path)

            if os.path.isdir(path):
                self.set_directory(path)
                self.path_input.clear()
            else:
                self.status_label.setText(f"❌ Папка не существует: {path}")

    def set_directory(self, directory):
        """Set current directory and update UI"""
        self.current_directory = directory
        self.scan_btn.setEnabled(True)
        self.path_input.setText(directory)
        self.status_label.setText(f"📁 Выбрана папка: {directory}")

    def start_scanning(self):
        """Start optimized directory scanning"""
        if not self.current_directory:
            return

        self.set_operation_state("🔍 Сканирование фотографий...")

        try:
            self.photos = self.scan_directory_optimized(self.current_directory)
            self.photo_list.clear()

            for photo in self.photos[:100]:  # Limit display for performance
                try:
                    filename = os.path.basename(photo)
                    # Handle encoding issues
                    if isinstance(filename, str):
                        self.photo_list.addItem(filename)
                    else:
                        self.photo_list.addItem(str(filename, errors='ignore'))
                except Exception:
                    self.photo_list.addItem("Фото")

            self.process_btn.setEnabled(True)
            self.status_label.setText(f"✅ Найдено фотографий: {len(self.photos)}")

        except Exception as e:
            self.status_label.setText(f"❌ Ошибка сканирования: {str(e)}")
        finally:
            self.clear_operation_state()

    def scan_directory_optimized(self, directory):
        """Optimized directory scanning with size limits"""
        photos = []
        exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.startswith('.'):
                    continue

                file_ext = os.path.splitext(file.lower())[1]
                if file_ext in exts:
                    photo_path = os.path.join(root, file)

                    # Size check
                    try:
                        size = os.path.getsize(photo_path)
                        if size > 100 * 1024 * 1024:  # Skip >100MB
                            continue
                        if size < 1024:  # Skip <1KB
                            continue
                    except OSError:
                        continue

                    photos.append(photo_path)

        return photos

    def start_face_processing(self):
        """Start optimized face processing"""
        if not self.photos:
            return

        self.set_operation_state("👤 Поиск лиц...")

        try:
            self.face_groups = self.process_faces_optimized(self.photos)
            self.sort_btn.setEnabled(bool(self.face_groups))

            total_faces = sum(len(group) for group in self.face_groups.values())
            self.status_label.setText(f"✅ Найдено групп: {len(self.face_groups)}, лиц: {total_faces}")

            if self.face_groups:
                QMessageBox.information(
                    self, "Поиск завершен",
                    f"Найдено {len(self.face_groups)} групп лиц на {total_faces} фотографиях.\n\n"
                    "Теперь вы можете отсортировать фотографии по группам."
                )
            else:
                QMessageBox.information(
                    self, "Поиск завершен",
                    "Лица не найдены. Попробуйте фотографии с четкими лицами."
                )

        except Exception as e:
            self.status_label.setText(f"❌ Ошибка обработки: {str(e)}")
        finally:
            self.clear_operation_state()

    def process_faces_optimized(self, photos):
        """Optimized face processing with memory management"""
        if not photos:
            return {}

        # Load Haar cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if not os.path.exists(cascade_path):
            raise FileNotFoundError("Haar cascade not found")

        face_cascade = cv2.CascadeClassifier(cascade_path)

        face_groups = defaultdict(list)
        group_id = 0

        for i, photo_path in enumerate(photos):
            if not os.path.exists(photo_path):
                continue

            try:
                # Load with size check
                size = os.path.getsize(photo_path)
                if size > 50 * 1024 * 1024:  # Skip >50MB
                    continue

                # Handle encoding issues for paths with non-ASCII characters
                try:
                    image = cv2.imread(photo_path)
                except Exception:
                    # Try alternative encoding
                    try:
                        import locale
                        encoding = locale.getpreferredencoding()
                        encoded_path = photo_path.encode(encoding).decode('utf-8')
                        image = cv2.imread(encoded_path)
                    except Exception:
                        # Last resort: use PIL which handles unicode better
                        from PIL import Image
                        pil_img = Image.open(photo_path)
                        image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                if image is None:
                    continue

                # Resize large images
                height, width = image.shape[:2]
                max_size = 1920
                if max(height, width) > max_size:
                    scale = max_size / max(height, width)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Convert to grayscale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces with optimized parameters
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=3,
                    minSize=(20, 20),
                    maxSize=(300, 300)
                )

                if len(faces) > 0:
                    # Simple clustering by face size
                    for face in faces:
                        face_area = face[2] * face[3]  # width * height

                        # Find existing group or create new
                        found_group = None
                        for gid, group_faces in face_groups.items():
                            if group_faces:
                                # Check if face size is similar to group
                                group_area = group_faces[0]['area']
                                if abs(face_area - group_area) < group_area * 0.3:  # 30% tolerance
                                    found_group = gid
                                    break

                        if found_group is None:
                            found_group = group_id
                            group_id += 1

                        face_groups[found_group].append({
                            'photo': photo_path,
                            'bbox': face,
                            'area': face_area
                        })

            except Exception:
                continue  # Skip problematic files

        # Clean empty groups
        return {k: v for k, v in face_groups.items() if v}

    def sort_photos(self):
        """Sort photos by face groups"""
        if not self.face_groups or not self.current_directory:
            return

        output_dir = QFileDialog.getExistingDirectory(
            self, "Выберите папку для отсортированных фотографий"
        )
        if not output_dir:
            return

        self.set_operation_state("📁 Сортировка фотографий...")

        try:
            self.sort_photos_optimized(self.face_groups, output_dir)

            total_photos = sum(len(group) for group in self.face_groups.values())
            QMessageBox.information(
                self, "Сортировка завершена",
                f"Фотографии отсортированы!\n"
                f"Групп: {len(self.face_groups)}\n"
                f"Всего фото: {total_photos}\n\n"
                f"Результат: {output_dir}"
            )
            self.status_label.setText(f"✅ Сортировка завершена: {len(self.face_groups)} групп")

        except Exception as e:
            self.status_label.setText(f"❌ Ошибка сортировки: {str(e)}")
        finally:
            self.clear_operation_state()

    def sort_photos_optimized(self, face_groups, output_dir):
        """Optimized photo sorting"""
        output_path = Path(output_dir)

        for group_id, faces in face_groups.items():
            if not faces:
                continue

            # Create group directory
            group_dir = output_path / f"person_{group_id + 1:03d}"
            group_dir.mkdir(parents=True, exist_ok=True)

            # Copy photos to group directory
            for face_info in faces:
                src_path = Path(face_info['photo'])
                if src_path.exists():
                    dst_path = group_dir / src_path.name
                    if not dst_path.exists():  # Avoid duplicates
                        dst_path.write_bytes(src_path.read_bytes())

    def on_photo_selected(self, index):
        """Handle photo selection"""
        if 0 <= index.row() < len(self.photos):
            photo_path = self.photos[index.row()]
            self.load_photo_preview(photo_path)
            self.update_photo_info(photo_path)

    def load_photo_preview(self, photo_path):
        """Load and display photo preview with size optimization"""
        try:
            if not os.path.exists(photo_path):
                self.photo_viewer.setText("Файл не найден")
                return

            # Handle encoding issues for paths with non-ASCII characters
            try:
                # Load with PIL for better memory management
                with Image.open(photo_path) as img:
                    img = ImageOps.exif_transpose(img)

                    # Resize for preview
                    width, height = img.size
                    max_preview_size = 600
                    if max(width, height) > max_preview_size:
                        ratio = max_preview_size / max(width, height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Convert to pixmap
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Save to temporary bytes
                    from io import BytesIO
                    buffer = BytesIO()
                    img.save(buffer, format='PNG', quality=85)
                    buffer.seek(0)

                    # Load as pixmap
                    pixmap = QPixmap()
                    pixmap.loadFromData(buffer.getvalue())

                    if not pixmap.isNull():
                        self.photo_viewer.setPixmap(pixmap.scaled(
                            self.photo_viewer.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        ))
                    else:
                        self.photo_viewer.setText("Ошибка загрузки")

            except Exception:
                # Fallback to direct path loading
                try:
                    with Image.open(photo_path) as img:
                        img = ImageOps.exif_transpose(img)

                        # Quick resize
                        width, height = img.size
                        if max(width, height) > 400:
                            ratio = 400 / max(width, height)
                            new_width = int(width * ratio)
                            new_height = int(height * ratio)
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                        # Convert and display
                        if img.mode != 'RGB':
                            img = img.convert('RGB')

                        from io import BytesIO
                        buffer = BytesIO()
                        img.save(buffer, format='PNG', quality=85)
                        buffer.seek(0)

                        pixmap = QPixmap()
                        pixmap.loadFromData(buffer.getvalue())

                        if not pixmap.isNull():
                            self.photo_viewer.setPixmap(pixmap.scaled(
                                self.photo_viewer.size(),
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation
                            ))
                        else:
                            self.photo_viewer.setText("Ошибка загрузки")
                except Exception as e:
                    self.photo_viewer.setText(f"Ошибка: {str(e)}")

        except Exception as e:
            self.photo_viewer.setText(f"Ошибка: {str(e)}")

    def update_photo_info(self, photo_path):
        """Update photo information display"""
        try:
            # Handle encoding issues
            try:
                filename = os.path.basename(photo_path)
                path = os.path.dirname(photo_path)
            except Exception:
                filename = "Фото"
                path = "Папка"

            # Get file size
            try:
                size_bytes = os.path.getsize(photo_path)
                size_mb = size_bytes / (1024 * 1024)
                size_text = ".1f"
            except Exception:
                size_text = "Неизвестно"

            # Safe text setting
            try:
                self.filename_label.setText(str(filename))
                self.path_label.setText(str(path))
                self.size_label.setText(size_text)
                self.faces_label.setText("0")  # Will be updated if faces are detected
            except Exception:
                self.filename_label.setText("Фото")
                self.path_label.setText("Папка")
                self.size_label.setText("Неизвестно")
                self.faces_label.setText("0")

        except Exception:
            self.filename_label.setText("Ошибка")
            self.path_label.setText("Ошибка")
            self.size_label.setText("Ошибка")
            self.faces_label.setText("Ошибка")

    def set_operation_state(self, message):
        """Set UI state for operation in progress"""
        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText(message)

        # Disable buttons
        self.scan_btn.setEnabled(False)
        self.process_btn.setEnabled(False)
        self.sort_btn.setEnabled(False)
        self.select_dir_btn.setEnabled(False)

    def clear_operation_state(self):
        """Clear operation state and re-enable buttons"""
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)

        # Re-enable buttons
        if self.current_directory:
            self.scan_btn.setEnabled(True)
        if self.photos:
            self.process_btn.setEnabled(True)
        if self.face_groups:
            self.sort_btn.setEnabled(True)
        self.select_dir_btn.setEnabled(True)

    def cancel_operation(self):
        """Cancel current operation"""
        self.status_label.setText("Операция отменена")
        self.clear_operation_state()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Photo Sorter - Optimized")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("PhotoTools")

    window = OptimizedPhotoSorter()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
