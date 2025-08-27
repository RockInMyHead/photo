"""
Main Window for Photo Sorting Application
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeView, QListView, QLabel, QPushButton, QProgressBar,
    QStatusBar, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QGroupBox, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QDir, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap
import os

from .photo_viewer import PhotoViewer
from .directory_scanner import DirectoryScanner
from .face_processor import FaceProcessor
from .photo_list_model import PhotoListModel
from .photo_sorter import PhotoSorter


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Sorter - Сортировка фотографий")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize components
        self.photo_viewer = PhotoViewer()
        self.directory_scanner = DirectoryScanner()
        self.face_processor = FaceProcessor()
        self.photo_sorter = PhotoSorter()
        self.photo_model = PhotoListModel()

        # Connect signals
        self.directory_scanner.progress_updated.connect(self.update_progress)
        self.directory_scanner.scanning_finished.connect(self.on_scanning_finished)
        self.face_processor.processing_finished.connect(self.on_face_processing_finished)
        self.photo_sorter.progress_updated.connect(self.update_progress)
        self.photo_sorter.sorting_finished.connect(self.on_sorting_finished)

        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()

    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Top control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Directory tree and photo list
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel - Photo viewer and details
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([400, 800])
        main_layout.addWidget(splitter)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

    def create_control_panel(self):
        """Create the top control panel"""
        group = QGroupBox("Управление")
        layout = QHBoxLayout(group)

        # Directory selection
        self.select_dir_btn = QPushButton("Выбрать папку с фотографиями")
        self.select_dir_btn.clicked.connect(self.select_directory)
        layout.addWidget(self.select_dir_btn)

        # Scan button
        self.scan_btn = QPushButton("Сканировать")
        self.scan_btn.clicked.connect(self.start_scanning)
        self.scan_btn.setEnabled(False)
        layout.addWidget(self.scan_btn)

        # Process faces button
        self.process_faces_btn = QPushButton("Обработать лица")
        self.process_faces_btn.clicked.connect(self.start_face_processing)
        self.process_faces_btn.setEnabled(False)
        layout.addWidget(self.process_faces_btn)

        # Sort button
        self.sort_btn = QPushButton("Сортировать по людям")
        self.sort_btn.clicked.connect(self.sort_photos)
        self.sort_btn.setEnabled(False)
        layout.addWidget(self.sort_btn)

        layout.addStretch()
        return group

    def create_left_panel(self):
        """Create the left panel with directory tree and photo list"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Directory tree
        layout.addWidget(QLabel("Папки:"))
        self.dir_tree = QTreeView()
        self.dir_tree.setMaximumHeight(200)
        layout.addWidget(self.dir_tree)

        # Photo list
        layout.addWidget(QLabel("Фотографии:"))
        self.photo_list = QListView()
        self.photo_list.setModel(self.photo_model)
        self.photo_list.clicked.connect(self.on_photo_selected)
        layout.addWidget(self.photo_list)

        return panel

    def create_right_panel(self):
        """Create the right panel with photo viewer and details"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Photo viewer
        layout.addWidget(QLabel("Просмотр фото:"))
        layout.addWidget(self.photo_viewer)

        # Photo details
        details_group = QGroupBox("Информация о фото")
        details_layout = QGridLayout(details_group)

        self.filename_label = QLabel("Файл:")
        self.path_label = QLabel("Путь:")
        self.size_label = QLabel("Размер:")
        self.faces_label = QLabel("Найдено лиц:")

        details_layout.addWidget(QLabel("Файл:"), 0, 0)
        details_layout.addWidget(self.filename_label, 0, 1)
        details_layout.addWidget(QLabel("Путь:"), 1, 0)
        details_layout.addWidget(self.path_label, 1, 1)
        details_layout.addWidget(QLabel("Размер:"), 2, 0)
        details_layout.addWidget(self.size_label, 2, 1)
        details_layout.addWidget(QLabel("Лица:"), 3, 0)
        details_layout.addWidget(self.faces_label, 3, 1)

        layout.addWidget(details_group)
        return panel

    def setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("Файл")

        open_action = QAction("Открыть папку...", self)
        open_action.triggered.connect(self.select_directory)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tools menu
        tools_menu = menubar.addMenu("Инструменты")

        scan_action = QAction("Сканировать фотографии", self)
        scan_action.triggered.connect(self.start_scanning)
        tools_menu.addAction(scan_action)

        process_action = QAction("Обработать лица", self)
        process_action.triggered.connect(self.start_face_processing)
        tools_menu.addAction(process_action)

        sort_action = QAction("Сортировать по людям", self)
        sort_action.triggered.connect(self.sort_photos)
        tools_menu.addAction(sort_action)

    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Готово")
        self.status_bar.addWidget(self.status_label)

    def select_directory(self):
        """Select directory containing photos"""
        directory = QFileDialog.getExistingDirectory(
            self, "Выберите папку с фотографиями"
        )

        if directory:
            self.current_directory = directory
            self.scan_btn.setEnabled(True)
            self.status_label.setText(f"Выбрана папка: {directory}")

    def start_scanning(self):
        """Start scanning directory for photos"""
        if not hasattr(self, 'current_directory'):
            return

        self.progress_bar.setVisible(True)
        self.status_label.setText("Сканирование фотографий...")

        self.directory_scanner.scan_directory(self.current_directory)

    def start_face_processing(self):
        """Start face detection and recognition"""
        if not hasattr(self.directory_scanner, 'photos') or not self.directory_scanner.photos:
            return

        self.progress_bar.setVisible(True)
        self.status_label.setText("Обработка лиц...")

        self.face_processor.process_photos(self.directory_scanner.photos)

    def sort_photos(self):
        """Sort photos by detected people"""
        if not hasattr(self.face_processor, 'face_groups') or not self.face_processor.face_groups:
            QMessageBox.information(self, "Информация",
                                  "Сначала необходимо обработать фотографии для поиска лиц.")
            return

        # Ask user for output directory
        output_dir = QFileDialog.getExistingDirectory(
            self, "Выберите папку для отсортированных фотографий"
        )

        if not output_dir:
            return

        self.progress_bar.setVisible(True)
        self.status_label.setText("Сортировка фотографий...")

        self.photo_sorter.sort_photos(
            self.face_processor.face_groups,
            output_dir,
            self.face_processor.group_names
        )

    def on_photo_selected(self, index):
        """Handle photo selection in the list"""
        photo_path = self.photo_model.get_photo_path(index.row())
        if photo_path:
            self.photo_viewer.load_photo(photo_path)
            self.update_photo_info(photo_path)

    def update_photo_info(self, photo_path):
        """Update photo information display"""
        filename = os.path.basename(photo_path)
        path = os.path.dirname(photo_path)

        # Get file size
        size_bytes = os.path.getsize(photo_path)
        size_mb = size_bytes / (1024 * 1024)
        size_text = ".1f"

        self.filename_label.setText(filename)
        self.path_label.setText(path)
        self.size_label.setText(size_text)

        # Check if faces were detected for this photo
        if hasattr(self.face_processor, 'photo_faces'):
            faces_count = len(self.face_processor.photo_faces.get(photo_path, []))
            self.faces_label.setText(str(faces_count))
        else:
            self.faces_label.setText("0")

    def update_progress(self, value, text):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        if text:
            self.status_label.setText(text)

    def on_scanning_finished(self, photos):
        """Handle completion of directory scanning"""
        self.progress_bar.setVisible(False)
        self.process_faces_btn.setEnabled(True)
        self.photo_model.update_photos(photos)
        self.status_label.setText(f"Найдено фотографий: {len(photos)}")

    def on_face_processing_finished(self, face_groups):
        """Handle completion of face processing"""
        self.progress_bar.setVisible(False)
        self.sort_btn.setEnabled(True)
        self.status_label.setText(f"Найдено групп лиц: {len(face_groups)}")

    def on_sorting_finished(self, sorted_groups):
        """Handle completion of photo sorting"""
        self.progress_bar.setVisible(False)

        if sorted_groups:
            total_photos = sum(len(photos) for photos in sorted_groups.values())
            QMessageBox.information(
                self, "Сортировка завершена",
                f"Фотографии успешно отсортированы!\n"
                f"Создано групп: {len(sorted_groups)}\n"
                f"Всего фотографий: {total_photos}"
            )
            self.status_label.setText(f"Сортировка завершена: {len(sorted_groups)} групп")
        else:
            QMessageBox.warning(self, "Предупреждение", "Не удалось отсортировать фотографии.")
            self.status_label.setText("Сортировка не удалась")
