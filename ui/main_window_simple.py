"""
Main Window for Photo Sorting Application - Simple Version
Uses OpenCV face detection without face-recognition library
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeView, QListView, QLabel, QPushButton, QProgressBar,
    QStatusBar, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QGroupBox, QGridLayout, QScrollArea, QLineEdit
)
from PyQt6.QtCore import Qt, QDir, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap
import os

from .photo_viewer import PhotoViewer
from .directory_scanner import DirectoryScanner
from .face_processor_simple import SimpleFaceProcessor
from .photo_list_model import PhotoListModel
from .photo_sorter import PhotoSorter
from .insight_sorter import InsightFaceSorter
from .queue_manager import QueueManager, ProcessingJob, JobStatus, QueueWidget
from .modern_styles import MODERN_STYLESHEET, COLORS, apply_button_style, apply_label_style


class MainWindow(QMainWindow):
    """Main application window - Simple version"""

    def __init__(self):
        try:
            print("Инициализация MainWindow...")
            super().__init__()
            self.setWindowTitle("🖼️ Photo Sorter - Умная сортировка фотографий")
            self.setGeometry(100, 100, 1400, 900)
            
            # Apply modern styling
            self.setStyleSheet(MODERN_STYLESHEET)
            print("Современный стиль применен")

            # Initialize components
            print("Инициализация компонентов...")
            self.photo_viewer = PhotoViewer()
            print("PhotoViewer создан")
            self.directory_scanner = DirectoryScanner()
            print("DirectoryScanner создан")
            self.face_processor = SimpleFaceProcessor()
            print("SimpleFaceProcessor создан")
            self.photo_sorter = PhotoSorter()
            print("PhotoSorter создан")

            # Initialize queue manager
            self.queue_manager = QueueManager()
            print("QueueManager создан")

            # Initialize InsightFaceSorter with error handling
            try:
                self.insight_sorter = InsightFaceSorter()
                print("InsightFaceSorter создан")
            except Exception as e:
                print(f"InsightFaceSorter недоступен: {e}")
                self.insight_sorter = None
            self.photo_model = PhotoListModel()
            print("PhotoListModel создан")

            # Connect signals
            print("Подключение сигналов...")
            self.directory_scanner.progress_updated.connect(self.update_progress)
            self.directory_scanner.scanning_finished.connect(self.on_scanning_finished)
            self.face_processor.progress_updated.connect(self.update_progress)
            self.face_processor.processing_finished.connect(self.on_face_processing_finished)
            self.photo_sorter.progress_updated.connect(self.update_progress)
            self.photo_sorter.sorting_finished.connect(self.on_sorting_finished)

            # Connect InsightFaceSorter signals only if available
            if self.insight_sorter is not None:
                self.insight_sorter.progress_updated.connect(self.update_progress)
                self.insight_sorter.sorting_finished.connect(self.on_insight_finished)
                self.insight_sorter.error_signal.connect(self.on_insight_error)
            print("Сигналы подключены")

            # Setup UI
            print("Настройка пользовательского интерфейса...")
            self.setup_ui()
            print("UI настроен")
            
        except Exception as e:
            print(f"Ошибка в __init__ MainWindow: {e}")
            import traceback
            traceback.print_exc()
            raise

    def cancel_operation(self):
        """Cancel current operation"""
        self.directory_scanner.requestInterruption()
        self.face_processor.requestInterruption()
        self.photo_sorter.requestInterruption()
        if self.insight_sorter is not None:
            self.insight_sorter.requestInterruption()

        self.status_label.setText("Операция отменена")
        self.enable_buttons()
        self.hide_progress()

        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()

    def enable_buttons(self):
        """Enable all control buttons"""
        self.scan_btn.setEnabled(True)
        if hasattr(self.directory_scanner, 'photos') and self.directory_scanner.photos:
            self.process_faces_btn.setEnabled(True)
            # Only enable InsightFace button if sorter is available
            if self.insight_sorter is not None:
                self.sort_insight_btn.setEnabled(True)
            else:
                self.sort_insight_btn.setEnabled(False)
        if hasattr(self.face_processor, 'face_groups') and self.face_processor.face_groups:
            self.sort_btn.setEnabled(True)

    def hide_progress(self):
        """Hide progress bar and cancel button"""
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)

    def setup_ui(self):
        """Setup the main user interface"""
        try:
            print("Настройка UI...")
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            print("Центральный виджет создан")

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

            # Progress bar and cancel button
            progress_layout = QHBoxLayout()
            self.progress_bar = QProgressBar()
            self.progress_bar.setVisible(False)
            progress_layout.addWidget(self.progress_bar)

            self.cancel_btn = QPushButton("Отмена")
            self.cancel_btn.setVisible(False)
            self.cancel_btn.clicked.connect(self.cancel_operation)
            progress_layout.addWidget(self.cancel_btn)

            main_layout.addLayout(progress_layout)

        except Exception as e:
            print(f"Ошибка в setup_ui: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Setup menu and status bar regardless of UI setup success
            try:
                self.setup_menu()
                self.setup_status_bar()
            except Exception as e:
                print(f"Ошибка в setup_menu/status_bar: {e}")

    def create_control_panel(self):
        """Create the top control panel"""
        group = QGroupBox("🎯 Управление")
        layout = QVBoxLayout(group)

        # Directory selection section
        dir_section = QGroupBox("📁 Выбор папки")
        dir_layout = QVBoxLayout(dir_section)
        
        # Directory selection row
        dir_row_layout = QHBoxLayout()
        
        self.select_dir_btn = QPushButton("📂 Выбрать папку")
        self.select_dir_btn.clicked.connect(self.select_directory)
        apply_button_style(self.select_dir_btn, "large")
        dir_row_layout.addWidget(self.select_dir_btn)

        # Manual path input
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("💡 ИЛИ введите путь вручную (например: D:\\Фотографии)")
        self.path_input.returnPressed.connect(self.manual_path_entered)
        dir_row_layout.addWidget(self.path_input)

        dir_layout.addLayout(dir_row_layout)
        layout.addWidget(dir_section)

        # Quick action section
        quick_section = QGroupBox("🚀 Быстрый запуск")
        quick_layout = QHBoxLayout(quick_section)
        
        # Main START button
        self.start_btn = QPushButton("🎬 СТАРТ - Полная обработка")
        self.start_btn.clicked.connect(self.start_full_processing)
        self.start_btn.setEnabled(False)
        apply_button_style(self.start_btn, "large success")
        quick_layout.addWidget(self.start_btn)
        
        # Output directory button
        self.output_btn = QPushButton("📤 Папка результата")
        self.output_btn.clicked.connect(self.select_output_directory)
        self.output_btn.setEnabled(False)
        quick_layout.addWidget(self.output_btn)
        
        layout.addWidget(quick_section)

        # Manual control section
        manual_section = QGroupBox("⚙️ Ручное управление")
        manual_layout = QVBoxLayout(manual_section)
        
        # First row of manual buttons
        buttons_row1 = QHBoxLayout()
        
        self.scan_btn = QPushButton("🔍 Сканировать")
        self.scan_btn.clicked.connect(self.start_scanning)
        self.scan_btn.setEnabled(False)
        buttons_row1.addWidget(self.scan_btn)

        self.process_faces_btn = QPushButton("👤 Найти лица")
        self.process_faces_btn.clicked.connect(self.start_face_processing)
        self.process_faces_btn.setEnabled(False)
        buttons_row1.addWidget(self.process_faces_btn)

        manual_layout.addLayout(buttons_row1)
        
        # Second row of manual buttons
        buttons_row2 = QHBoxLayout()
        
        self.sort_btn = QPushButton("📋 Сортировать по группам")
        self.sort_btn.clicked.connect(self.sort_photos)
        self.sort_btn.setEnabled(False)
        buttons_row2.addWidget(self.sort_btn)

        # Insight sort button (move-only)
        insight_text = "🧠 InsightFace (точная сортировка)"
        if self.insight_sorter is None:
            insight_text += " [НЕДОСТУПЕН]"
        self.sort_insight_btn = QPushButton(insight_text)
        self.sort_insight_btn.clicked.connect(self.sort_photos_insight)
        self.sort_insight_btn.setEnabled(False)
        apply_button_style(self.sort_insight_btn, "warning" if self.insight_sorter is None else "")
        buttons_row2.addWidget(self.sort_insight_btn)

        manual_layout.addLayout(buttons_row2)
        layout.addWidget(manual_section)

        # Info section
        info_section = QGroupBox("ℹ️ Информация")
        info_layout = QVBoxLayout(info_section)
        
        info_label = QLabel("✨ Используется базовое распознавание лиц OpenCV")
        apply_label_style(info_label, "caption")
        info_layout.addWidget(info_label)
        
        if self.insight_sorter is None:
            warning_label = QLabel("⚠️ Для точной сортировки установите: pip install insightface onnxruntime")
            apply_label_style(warning_label, "warning")
            info_layout.addWidget(warning_label)
        
        layout.addWidget(info_section)

        return group

    def create_left_panel(self):
        """Create the left panel with directory tree, photo list and queue"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Directory tree section
        dir_section = QGroupBox("📂 Структура папок")
        dir_section_layout = QVBoxLayout(dir_section)
        self.dir_tree = QTreeView()
        self.dir_tree.setMaximumHeight(180)
        dir_section_layout.addWidget(self.dir_tree)
        layout.addWidget(dir_section)

        # Photo list section
        photos_section = QGroupBox("🖼️ Найденные фотографии")
        photos_section_layout = QVBoxLayout(photos_section)
        self.photo_list = QListView()
        self.photo_list.setModel(self.photo_model)
        self.photo_list.clicked.connect(self.on_photo_selected)
        photos_section_layout.addWidget(self.photo_list)
        layout.addWidget(photos_section)

        # Queue section
        queue_section = QGroupBox("⏳ Очередь обработки")
        queue_section_layout = QVBoxLayout(queue_section)
        self.queue_widget = QueueWidget(self.queue_manager)
        queue_section_layout.addWidget(self.queue_widget)
        layout.addWidget(queue_section)

        return panel

    def create_right_panel(self):
        """Create the right panel with photo viewer and details"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Photo viewer section
        viewer_section = QGroupBox("🖼️ Предварительный просмотр")
        viewer_layout = QVBoxLayout(viewer_section)
        viewer_layout.addWidget(self.photo_viewer)
        layout.addWidget(viewer_section)

        # Photo details section
        details_group = QGroupBox("📋 Информация о фотографии")
        details_layout = QGridLayout(details_group)

        # Create styled labels
        self.filename_label = QLabel("-")
        self.path_label = QLabel("-")
        self.size_label = QLabel("-")
        self.faces_label = QLabel("-")

        # Style the info labels
        apply_label_style(self.filename_label, "subtitle")
        apply_label_style(self.path_label, "caption")
        apply_label_style(self.size_label, "caption")
        apply_label_style(self.faces_label, "success")

        # Create field labels
        file_lbl = QLabel("📄 Файл:")
        path_lbl = QLabel("📁 Путь:")
        size_lbl = QLabel("📏 Размер:")
        faces_lbl = QLabel("👤 Лица:")

        apply_label_style(file_lbl, "caption")
        apply_label_style(path_lbl, "caption")
        apply_label_style(size_lbl, "caption")
        apply_label_style(faces_lbl, "caption")

        details_layout.addWidget(file_lbl, 0, 0)
        details_layout.addWidget(self.filename_label, 0, 1)
        details_layout.addWidget(path_lbl, 1, 0)
        details_layout.addWidget(self.path_label, 1, 1)
        details_layout.addWidget(size_lbl, 2, 0)
        details_layout.addWidget(self.size_label, 2, 1)
        details_layout.addWidget(faces_lbl, 3, 0)
        details_layout.addWidget(self.faces_label, 3, 1)

        # Progress info section
        progress_group = QGroupBox("📊 Статистика обработки")
        progress_layout = QVBoxLayout(progress_group)
        
        self.stats_label = QLabel("Готов к работе")
        apply_label_style(self.stats_label, "caption")
        progress_layout.addWidget(self.stats_label)
        
        layout.addWidget(details_group)
        layout.addWidget(progress_group)
        
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

        process_action = QAction("Найти лица", self)
        process_action.triggered.connect(self.start_face_processing)
        tools_menu.addAction(process_action)

        sort_action = QAction("Сортировать по группам", self)
        sort_action.triggered.connect(self.sort_photos)
        tools_menu.addAction(sort_action)

    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Готово (простая версия)")
        self.status_bar.addWidget(self.status_label)

    def select_directory(self):
        """Select directory containing photos"""
        try:
            directory = QFileDialog.getExistingDirectory(
                self, "Выберите папку с фотографиями"
            )
        except Exception as e:
            # Fallback: try without parent widget
            directory = QFileDialog.getExistingDirectory(
                None, "Выберите папку с фотографиями"
            )

        if directory:
            self.set_directory(directory)
        else:
            self.status_label.setText("Папка не выбрана")

    def manual_path_entered(self):
        """Handle manual path input"""
        path = self.path_input.text().strip()
        if path:
            # Expand ~ for home directory
            path = os.path.expanduser(path)
            # Convert to absolute path
            path = os.path.abspath(path)

            if os.path.isdir(path):
                self.set_directory(path)
                self.path_input.clear()
            else:
                self.status_label.setText(f"Папка не существует: {path}")

    def set_directory(self, directory):
        """Set the current directory and update UI"""
        self.current_directory = directory
        self.scan_btn.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.output_btn.setEnabled(True)
        # Only enable InsightFace button if sorter is available
        if self.insight_sorter is not None:
            self.sort_insight_btn.setEnabled(True)
        self.path_input.setText(directory)
        self.status_label.setText(f"📂 Выбрана папка: {directory}")
        self.stats_label.setText(f"Входная папка: {os.path.basename(directory)}")

    def select_output_directory(self):
        """Select output directory for sorted photos"""
        try:
            directory = QFileDialog.getExistingDirectory(
                self, "Выберите папку для результатов сортировки"
            )
        except Exception as e:
            directory = QFileDialog.getExistingDirectory(
                None, "Выберите папку для результатов сортировки"
            )

        if directory:
            self.output_directory = directory
            self.output_btn.setText(f"📤 {os.path.basename(directory)}")
            apply_button_style(self.output_btn, "success")
            self.status_label.setText(f"📤 Папка результата: {directory}")
        else:
            self.status_label.setText("Папка результата не выбрана")

    def start_full_processing(self):
        """Start full automated processing"""
        if not hasattr(self, 'current_directory'):
            QMessageBox.information(self, "Информация", "Сначала выберите входную папку с фотографиями.")
            return

        if not hasattr(self, 'output_directory'):
            QMessageBox.information(self, "Информация", "Сначала выберите папку для результатов.")
            return

        # Create a full processing job
        import uuid
        job = ProcessingJob(
            job_id=str(uuid.uuid4()),
            input_path=self.current_directory,
            output_path=self.output_directory,
            job_type="full_process"
        )

        # Add to queue
        self.queue_manager.add_job(job)
        
        # Update UI
        self.status_label.setText("🚀 Запущена полная обработка...")
        self.stats_label.setText("Задача добавлена в очередь")
        
        # Show info
        QMessageBox.information(
            self, "Обработка запущена",
            f"Полная обработка добавлена в очередь!\n\n"
            f"Входная папка: {self.current_directory}\n"
            f"Выходная папка: {self.output_directory}\n\n"
            f"Процесс включает:\n"
            f"• Сканирование фотографий\n"
            f"• Обнаружение лиц\n"
            f"• Группировка по людям\n"
            f"• Создание папок и сортировка"
        )

    def start_scanning(self):
        """Start scanning directory for photos"""
        if not hasattr(self, 'current_directory'):
            return

        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Сканирование фотографий...")

        # Disable buttons during operation
        self.scan_btn.setEnabled(False)
        self.process_faces_btn.setEnabled(False)
        self.sort_btn.setEnabled(False)
        self.sort_insight_btn.setEnabled(False)

        self.directory_scanner.scan_directory(self.current_directory)

    def start_face_processing(self):
        """Start face detection using OpenCV"""
        if not hasattr(self.directory_scanner, 'photos') or not self.directory_scanner.photos:
            return

        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Поиск лиц с помощью OpenCV...")

        # Disable buttons during operation
        self.scan_btn.setEnabled(False)
        self.process_faces_btn.setEnabled(False)
        self.sort_btn.setEnabled(False)
        self.sort_insight_btn.setEnabled(False)

        self.face_processor.process_photos(self.directory_scanner.photos)

    def sort_photos(self):
        """Sort photos by detected people"""
        if not hasattr(self.face_processor, 'face_groups') or not self.face_processor.face_groups:
            QMessageBox.information(self, "Информация",
                                  "Сначала необходимо найти лица на фотографиях.")
            return

        # Ask user for output directory
        output_dir = QFileDialog.getExistingDirectory(
            self, "Выберите папку для отсортированных фотографий"
        )

        if not output_dir:
            return

        self.progress_bar.setVisible(True)
        self.status_label.setText("Сортировка фотографий по группам...")

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
        size_text = f"{size_mb:.1f} МБ" if size_mb >= 1 else f"{size_bytes / 1024:.1f} КБ"

        self.filename_label.setText(filename)
        self.path_label.setText(path)
        self.size_label.setText(size_text)

        # Check if faces were detected for this photo
        if hasattr(self.face_processor, 'photo_faces'):
            faces_count = len(self.face_processor.photo_faces.get(photo_path, []))
            self.faces_label.setText(str(faces_count))
            if faces_count > 0:
                apply_label_style(self.faces_label, "success")
            else:
                apply_label_style(self.faces_label, "caption")
        else:
            self.faces_label.setText("0")
            apply_label_style(self.faces_label, "caption")

    def update_progress(self, value, text):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        if text:
            self.status_label.setText(text)

    def on_scanning_finished(self, photos):
        """Handle completion of directory scanning"""
        self.hide_progress()
        self.enable_buttons()
        self.photo_model.update_photos(photos)
        self.status_label.setText(f"📸 Найдено фотографий: {len(photos)}")
        self.stats_label.setText(f"Отсканировано: {len(photos)} файлов")

    def on_face_processing_finished(self, face_groups):
        """Handle completion of face processing"""
        self.hide_progress()
        self.enable_buttons()

        total_faces = sum(len(group) for group in face_groups.values())
        self.status_label.setText(f"👥 Найдено групп: {len(face_groups)}, всего лиц: {total_faces}")
        self.stats_label.setText(f"Распознано: {len(face_groups)} групп, {total_faces} лиц")

        if face_groups:
            QMessageBox.information(
                self, "🎉 Поиск завершен",
                f"Найдено {len(face_groups)} групп лиц на {total_faces} фотографиях.\n\n"
                "✅ Теперь вы можете отсортировать фотографии по группам."
            )
        else:
            QMessageBox.information(
                self, "⚠️ Поиск завершен",
                "Лица не найдены на фотографиях.\n\n"
                "💡 Попробуйте использовать фотографии с четкими лицами анфас."
            )

    def on_sorting_finished(self, sorted_groups):
        """Handle completion of photo sorting"""
        self.hide_progress()
        self.enable_buttons()

        if sorted_groups:
            total_photos = sum(len(photos) for photos in sorted_groups.values())
            QMessageBox.information(
                self, "Сортировка завершена",
                f"Фотографии успешно отсортированы!\n"
                f"Создано групп: {len(sorted_groups)}\n"
                f"Всего фотографий: {total_photos}\n\n"
                f"Каждая группа сохранена в отдельной папке."
            )
            self.status_label.setText(f"Сортировка завершена: {len(sorted_groups)} групп")
        else:
            QMessageBox.warning(self, "Предупреждение", "Не удалось отсортировать фотографии.")
            self.status_label.setText("Сортировка не удалась")

    def sort_photos_insight(self):
        """Run InsightFace-based sort with move-only export"""
        if self.insight_sorter is None:
            QMessageBox.warning(self, "InsightFace недоступен",
                              "InsightFace не установлен. Установите: pip install insightface onnxruntime hdbscan scikit-learn tqdm")
            return

        if not hasattr(self, 'current_directory'):
            QMessageBox.information(self, "Информация", "Сначала выберите папку с фотографиями.")
            return

        output_dir = QFileDialog.getExistingDirectory(
            self, "Выберите папку результата (перенос файлов)"
        )
        if not output_dir:
            return

        self.progress_bar.setVisible(True)
        self.cancel_btn.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("InsightFace: детекция и перенос...")

        # Disable buttons during operation
        self.scan_btn.setEnabled(False)
        self.process_faces_btn.setEnabled(False)
        self.sort_btn.setEnabled(False)
        self.sort_insight_btn.setEnabled(False)

        # Device: CPU by default
        self.insight_sorter.sort_with_insight(
            input_dir=self.current_directory,
            output_dir=output_dir,
            device="cpu"
        )

    def on_insight_finished(self, stats: dict):
        self.hide_progress()
        self.enable_buttons()

        if not stats.get("ok"):
            QMessageBox.warning(self, "InsightFace", f"Ошибка: {stats.get('error', 'Неизвестно')}")
            self.status_label.setText("InsightFace: ошибка")
            return
        groups = stats.get("groups", 0)
        moved = stats.get("moved", 0)
        out_dir = stats.get("out", "")
        QMessageBox.information(
            self, "InsightFace",
            f"Готово! Перемещено файлов: {moved}\nСоздано групп: {groups}\nВыход: {out_dir}"
        )
        self.status_label.setText(f"InsightFace: {groups} групп, {moved} переносов")

    def on_insight_error(self, message: str):
        self.hide_progress()
        self.enable_buttons()

        QMessageBox.warning(
            self, "InsightFace зависимости",
            message + "\n\nУстановите: pip install -r requirements_insight.txt"
        )
        self.status_label.setText("InsightFace: отсутствуют зависимости")
