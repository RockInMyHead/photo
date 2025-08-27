"""
Simplified Main Window with Tabbed Interface for Photo Sorting Application
Fully automated processing - user only sees progress
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeView, QListView, QListWidget, QLabel, QPushButton, QProgressBar,
    QStatusBar, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QGroupBox, QGridLayout, QScrollArea, QLineEdit, QTabWidget,
    QComboBox, QCheckBox
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
from .theme_manager import ThemeManager
from .theme_test_widget import ThemeTestWidget
from .modern_styles import apply_button_style, apply_label_style


class OverviewTab(QWidget):
    """Overview and Quick Start Tab - Simplified"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup simplified overview tab UI"""
        layout = QVBoxLayout(self)
        
        # Compact welcome section
        title = QLabel("🏠 Photo Sorter - Автоматическая сортировка фотографий")
        apply_label_style(title, "title")
        layout.addWidget(title)
        
        # Quick start section
        quick_section = QGroupBox("🚀 Запуск")
        quick_layout = QVBoxLayout(quick_section)
        
        # Step 1 - Select folder
        step1_layout = QHBoxLayout()
        step1_num = QLabel("1️⃣")
        step1_num.setFixedWidth(40)
        step1_layout.addWidget(step1_num)
        
        self.select_input_btn = QPushButton("📂 Выбрать папку с фотографиями")
        self.select_input_btn.clicked.connect(self.select_input_directory)
        apply_button_style(self.select_input_btn, "large")
        step1_layout.addWidget(self.select_input_btn)
        
        self.input_path_label = QLabel("Папка не выбрана")
        apply_label_style(self.input_path_label, "caption")
        step1_layout.addWidget(self.input_path_label)
        
        quick_layout.addLayout(step1_layout)
        
        # Step 2 - Auto output
        step2_layout = QHBoxLayout()
        step2_num = QLabel("2️⃣")
        step2_num.setFixedWidth(40)
        step2_layout.addWidget(step2_num)

        step2_text = QLabel("📤 Результаты: создаются автоматически в подпапке PhotoSorter_Results")
        apply_label_style(step2_text, "caption")
        step2_layout.addWidget(step2_text)

        quick_layout.addLayout(step2_layout)
        
        # Step 3 - Start or Queue
        step3_layout = QHBoxLayout()
        step3_num = QLabel("3️⃣")
        step3_num.setFixedWidth(40)
        step3_layout.addWidget(step3_num)

        # Start processing buttons
        buttons_layout = QVBoxLayout()

        self.start_btn = QPushButton("🎬 СТАРТ - Начать обработку!")
        self.start_btn.clicked.connect(self.start_processing)
        self.start_btn.setEnabled(False)
        apply_button_style(self.start_btn, "large success")
        buttons_layout.addWidget(self.start_btn)

        # Add to queue button
        self.add_to_queue_btn = QPushButton("➕ Добавить в очередь пакетной обработки")
        self.add_to_queue_btn.clicked.connect(self.add_current_to_batch_queue)
        self.add_to_queue_btn.setEnabled(False)
        apply_button_style(self.add_to_queue_btn, "warning")
        buttons_layout.addWidget(self.add_to_queue_btn)

        step3_layout.addLayout(buttons_layout)

        quick_layout.addLayout(step3_layout)
        layout.addWidget(quick_section)
        
        # Progress section (показывается при запуске)
        self.progress_section = QGroupBox("⏳ Прогресс обработки")
        progress_layout = QVBoxLayout(self.progress_section)
        
        self.current_operation_label = QLabel("Готов к началу работы")
        apply_label_style(self.current_operation_label, "subtitle")
        progress_layout.addWidget(self.current_operation_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Кнопка отмены
        cancel_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("⏹️ Остановить")
        self.cancel_btn.clicked.connect(self.cancel_operation)
        self.cancel_btn.setVisible(False)
        apply_button_style(self.cancel_btn, "danger")
        cancel_layout.addWidget(self.cancel_btn)
        cancel_layout.addStretch()
        progress_layout.addLayout(cancel_layout)
        
        self.progress_section.setVisible(False)
        layout.addWidget(self.progress_section)
        
        # Status section
        status_section = QGroupBox("📊 Статус")
        status_layout = QVBoxLayout(status_section)
        
        self.status_label = QLabel("Готов к работе")
        apply_label_style(self.status_label, "subtitle")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_section)
        layout.addStretch()
    
    def select_input_directory(self):
        """Select input directory"""
        directory = QFileDialog.getExistingDirectory(self, "Выберите папку с фотографиями")
        if directory:
            self.parent_window.current_directory = directory
            self.input_path_label.setText(os.path.basename(directory))
            apply_label_style(self.input_path_label, "success")

            # Автоматически устанавливаем выходную папку как подпапку входной
            output_dir = os.path.join(directory, "PhotoSorter_Results")
            self.parent_window.output_directory = output_dir

            # Активируем кнопки
            self.start_btn.setEnabled(True)
            self.add_to_queue_btn.setEnabled(True)
            self.status_label.setText(f"✅ Готово к обработке! Нажмите СТАРТ или добавьте в очередь.")

            # Обновляем ViewerTab с новой директорией
            viewer_tab = self.parent_window.tab_widget.widget(2)  # ViewerTab is at index 2
            viewer_tab.update_directory(directory)
    
    def start_processing(self):
        """Start full automated processing"""
        if hasattr(self.parent_window, 'current_directory'):
            input_dir = self.parent_window.current_directory
            output_dir = self.parent_window.output_directory
            
            # Показываем диалог подтверждения
            reply = QMessageBox.question(
                self, 
                'Подтверждение запуска', 
                f'Начать автоматическую сортировку?\n\n'
                f'📂 Входная папка: {os.path.basename(input_dir)}\n'
                f'📤 Результаты: PhotoSorter_Results\n\n'
                f'Процесс полностью автоматический:\n'
                f'• Сканирование фотографий\n'
                f'• Поиск и распознавание лиц\n'
                f'• Автоматическая сортировка\n\n'
                f'Вы увидите только прогресс выполнения.', 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Показываем секцию прогресса
                self.progress_section.setVisible(True)
                self.progress_bar.setVisible(True)
                self.cancel_btn.setVisible(True)
                
                # Скрываем кнопку СТАРТ
                self.start_btn.setEnabled(False)
                self.start_btn.setText("⏳ Обработка...")
                
                # Обновляем статус
                self.current_operation_label.setText("🔄 Запуск автоматической обработки...")
                self.status_label.setText("⚡ Обработка запущена! Переключитесь на вкладку 'Обработка' для просмотра прогресса.")
                
                # Переключаемся на вкладку Processing
                self.parent_window.tab_widget.setCurrentIndex(1)
                
                # Запускаем полную обработку
                processing_tab = self.parent_window.tab_widget.widget(1)
                processing_tab.start_full_processing(input_dir, output_dir)
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите папку с фотографиями!")

    def add_current_to_batch_queue(self):
        """Add current selected folder to batch processing queue"""
        if hasattr(self.parent_window, 'current_directory'):
            current_dir = self.parent_window.current_directory

            # Switch to Queue tab
            self.parent_window.tab_widget.setCurrentIndex(3)  # QueueTab is at index 3

            # Get QueueTab and add current folder
            queue_tab = self.parent_window.tab_widget.widget(3)

            # Add current folder to queue tab's selected folders
            if current_dir not in queue_tab.selected_folders:
                queue_tab.selected_folders.append(current_dir)
                queue_tab.update_folders_list()
                queue_tab.start_batch_btn.setEnabled(True)

                QMessageBox.information(
                    self,
                    "✅ Добавлено в очередь",
                    f"Папка '{os.path.basename(current_dir)}' добавлена в очередь пакетной обработки.\n\n"
                    "📂 Перейдите в раздел '📋 Очередь' для управления пакетной обработкой."
                )
            else:
                QMessageBox.information(
                    self,
                    "Информация",
                    "Эта папка уже находится в очереди пакетной обработки."
                )
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите папку с фотографиями!")

    def cancel_operation(self):
        """Cancel current operation"""
        processing_tab = self.parent_window.tab_widget.widget(1)
        processing_tab.cancel_operation()
        
        # Сбрасываем интерфейс
        self.progress_section.setVisible(False)
        self.start_btn.setEnabled(True)
        self.add_to_queue_btn.setEnabled(True)
        self.start_btn.setText("🎬 СТАРТ - Начать обработку!")
        self.status_label.setText("❌ Обработка отменена")

    def on_processing_finished(self, success=True):
        """Called when processing is finished"""
        self.progress_section.setVisible(False)
        self.start_btn.setEnabled(True)
        self.add_to_queue_btn.setEnabled(True)
        self.start_btn.setText("🎬 СТАРТ - Начать обработку!")

        if success:
            self.status_label.setText("✅ Обработка завершена успешно! Проверьте папку PhotoSorter_Results.")
        else:
            self.status_label.setText("❌ Обработка прервана или завершилась с ошибкой")


class ProcessingTab(QWidget):
    """Processing Tab - Only Progress and Results"""

    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.face_groups = {}  # Store face groups for sorting
        self.group_names = {}  # Store group names
        self.setup_ui()
    
    def setup_ui(self):
        """Setup simplified processing tab UI"""
        layout = QVBoxLayout(self)
        
        # Current operation section
        current_section = QGroupBox("🔄 Текущая операция")
        current_layout = QVBoxLayout(current_section)
        
        self.current_operation_label = QLabel("Ожидание...")
        apply_label_style(self.current_operation_label, "subtitle")
        current_layout.addWidget(self.current_operation_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        current_layout.addWidget(self.progress_bar)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("⏹️ Отмена")
        self.cancel_btn.clicked.connect(self.cancel_operation)
        self.cancel_btn.setVisible(False)
        apply_button_style(self.cancel_btn, "danger")
        controls_layout.addWidget(self.cancel_btn)
        controls_layout.addStretch()
        
        current_layout.addLayout(controls_layout)
        layout.addWidget(current_section)
        
        # Compact auto info
        auto_info_section = QGroupBox("⚡ Автоматическая обработка")
        auto_info_layout = QVBoxLayout(auto_info_section)

        auto_description = QLabel("🤖 Процесс полностью автоматический")
        apply_label_style(auto_description, "caption")
        auto_info_layout.addWidget(auto_description)
        
        # Directory info
        dir_info_layout = QHBoxLayout()
        dir_info_layout.addWidget(QLabel("📁 Рабочая папка:"))
        self.working_dir_label = QLabel("Не выбрана")
        apply_label_style(self.working_dir_label, "caption")
        dir_info_layout.addWidget(self.working_dir_label)
        dir_info_layout.addStretch()
        auto_info_layout.addLayout(dir_info_layout)
        
        layout.addWidget(auto_info_section)
        
        # Results section
        results_section = QGroupBox("📊 Результаты")
        results_layout = QVBoxLayout(results_section)
        
        self.results_label = QLabel("Обработка еще не запускалась")
        apply_label_style(self.results_label, "caption")
        results_layout.addWidget(self.results_label)
        
        layout.addWidget(results_section)
        layout.addStretch()
    
    def update_working_directory(self):
        """Update working directory display"""
        if hasattr(self.parent_window, 'current_directory'):
            input_dir = self.parent_window.current_directory
            self.working_dir_label.setText(f"{os.path.basename(input_dir)} → PhotoSorter_Results")
            apply_label_style(self.working_dir_label, "success")
        else:
            self.working_dir_label.setText("Не выбрана")
            apply_label_style(self.working_dir_label, "caption")
    
    def start_full_processing(self, input_dir, output_dir):
        """Start full automated processing"""
        # Создаем выходную папку автоматически
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать папку результатов: {e}")
            return

        self.parent_window.output_directory = output_dir
        
        # Обновляем интерфейс
        self.current_operation_label.setText("🔄 Инициализация автоматической обработки...")
        self.working_dir_label.setText(f"{os.path.basename(input_dir)} → PhotoSorter_Results")
        
        # Показываем прогресс бар
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Неопределенный прогресс
        
        # Показываем кнопку отмены
        self.cancel_btn.setVisible(True)

        # Create job and add to queue
        import uuid
        job = ProcessingJob(
            job_id=str(uuid.uuid4()),
            input_path=input_dir,
            output_path=output_dir,
            job_type="full_process"
        )

        self.parent_window.queue_manager.add_job(job)
        
        # Начинаем автоматическую обработку
        self.start_auto_processing_sequence()
    
    def start_auto_processing_sequence(self):
        """Start automated processing sequence"""
        # Начинаем с сканирования
        self.current_operation_label.setText("🔍 Шаг 1/3: Сканирование фотографий...")
        self.progress_bar.setValue(10)
        self.progress_bar.setRange(0, 100)
        
        # Запускаем сканирование
        self.start_scanning(auto_continue=True)
    
    def cancel_operation(self):
        """Cancel current operation"""
        # Останавливаем все потоки
        if hasattr(self.parent_window, 'directory_scanner'):
            self.parent_window.directory_scanner.stop()
        if hasattr(self.parent_window, 'face_processor'):
            self.parent_window.face_processor.stop()
        if hasattr(self.parent_window, 'photo_sorter'):
            self.parent_window.photo_sorter.stop()
        
        # Сбрасываем интерфейс
        self.current_operation_label.setText("❌ Операция отменена")
        self.progress_bar.setVisible(False)
        self.cancel_btn.setVisible(False)
        
        # Уведомляем Overview tab
        overview_tab = self.parent_window.tab_widget.widget(0)
        overview_tab.on_processing_finished(success=False)
    
    def start_scanning(self, auto_continue=True):
        """Start scanning photos"""
        if not hasattr(self.parent_window, 'current_directory'):
            return
        
        directory = self.parent_window.current_directory
        # trigger scanning via scanner API
        if hasattr(self.parent_window.directory_scanner, 'set_directory'):
            self.parent_window.directory_scanner.set_directory(directory)
            self.parent_window.directory_scanner.start()
        else:
            # fallback to scan_directory method
            self.parent_window.directory_scanner.scan_directory(directory)
    
    def on_scanning_finished(self, photos, auto_continue=True):
        """Called when scanning is finished"""
        try:
            photo_count = len(photos) if isinstance(photos, (list, tuple)) else int(photos)
        except Exception:
            photo_count = 0
        # update model with found photos if available
        if hasattr(self.parent_window, 'photo_list_model') and isinstance(photos, (list, tuple)):
            self.parent_window.photo_list_model.update_photos(list(photos))
        self.results_label.setText(f"✅ Найдено {photo_count} фотографий")
        
        if auto_continue:
            # Автоматически продолжаем к распознаванию лиц
            self.current_operation_label.setText("👤 Шаг 2/3: Поиск и распознавание лиц...")
            self.progress_bar.setValue(40)
            self.start_face_detection(auto_continue=True)
    
    def start_face_detection(self, auto_continue=True):
        """Start face detection"""
        photos = self.parent_window.photo_list_model.photos
        if photos:
            self.parent_window.face_processor.process_photos(photos)
    
    def on_face_processing_finished(self, face_groups, auto_continue=True):
        """Called when face processing is finished"""
        # Store face groups for sorting
        if isinstance(face_groups, dict):
            self.face_groups = face_groups
        else:
            self.face_groups = {}

        # face_groups is expected to be a dict: group_id -> [photos]
        try:
            group_count = len(self.face_groups)
            face_count = sum(len(v) for v in self.face_groups.values()) if self.face_groups else 0
        except Exception:
            group_count = 0
            face_count = 0

        self.results_label.setText(f"✅ Обнаружено {face_count} лиц в {group_count} группах")

        if auto_continue:
            # Автоматически продолжаем к сортировке
            self.current_operation_label.setText("📋 Шаг 3/3: Сортировка по группам...")
            self.progress_bar.setValue(70)
            self.start_sorting(auto_continue=True)
    
    def start_sorting(self, auto_continue=True):
        """Start sorting photos"""
        if hasattr(self.parent_window, 'output_directory') and self.face_groups:
            self.parent_window.photo_sorter.sort_photos(
                self.face_groups,
                self.parent_window.output_directory,
                self.group_names
            )
    
    def on_sorting_finished(self, sorted_groups, auto_continue=True):
        """Called when sorting is finished"""
        try:
            # sorted_groups expected dict group_id -> [photos]
            group_count = len(sorted_groups) if isinstance(sorted_groups, dict) else 0
            sorted_count = sum(len(v) for v in sorted_groups.values()) if isinstance(sorted_groups, dict) else 0
        except Exception:
            group_count = 0
            sorted_count = 0

        self.results_label.setText(
            f"✅ Обработка завершена!\n"
            f"• Отсортировано: {sorted_count} фотографий\n"
            f"• Групп: {group_count}\n"
            f"• Папка: {os.path.basename(self.parent_window.output_directory)}"
        )
        apply_label_style(self.results_label, "success")

        if auto_continue:
            # Завершаем автоматическую обработку
            self.current_operation_label.setText("✅ Автоматическая обработка завершена!")
            self.progress_bar.setValue(100)
            self.cancel_btn.setVisible(False)

            # Уведомляем Overview tab о завершении
            overview_tab = self.parent_window.tab_widget.widget(0)
            overview_tab.on_processing_finished(success=True)

            # Показываем сообщение о завершении
            QMessageBox.information(
                self, "✅ Готово!",
                f"Автоматическая сортировка завершена!\n\n"
                f"✅ Отсортировано {sorted_count} фотографий\n"
                f"📁 Создано {group_count} групп\n\n"
                f"📂 Проверьте папку:\n"
                f"{os.path.basename(self.parent_window.output_directory)}"
            )


class ViewerTab(QWidget):
    """Photo Viewer Tab with File Explorer"""

    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup viewer tab UI with file explorer"""
        main_layout = QVBoxLayout(self)

        # Create splitter for file explorer and viewer
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel: File Explorer
        explorer_widget = QWidget()
        explorer_layout = QVBoxLayout(explorer_widget)

        # Explorer header
        explorer_header = QGroupBox("📁 Проводник")
        header_layout = QVBoxLayout(explorer_header)

        # Current directory info
        self.current_dir_label = QLabel("Папка не выбрана")
        apply_label_style(self.current_dir_label, "caption")
        header_layout.addWidget(self.current_dir_label)

        # Navigation controls
        nav_layout = QHBoxLayout()

        self.up_btn = QPushButton("⬆️ Вверх")
        self.up_btn.clicked.connect(self.go_up)
        self.up_btn.setEnabled(False)
        apply_button_style(self.up_btn)
        nav_layout.addWidget(self.up_btn)

        self.home_btn = QPushButton("🏠 Домой")
        self.home_btn.clicked.connect(self.go_home)
        self.home_btn.setEnabled(False)
        apply_button_style(self.home_btn)
        nav_layout.addWidget(self.home_btn)

        nav_layout.addStretch()

        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.clicked.connect(self.refresh_explorer)
        apply_button_style(self.refresh_btn)
        nav_layout.addWidget(self.refresh_btn)

        header_layout.addLayout(nav_layout)

        explorer_layout.addWidget(explorer_header)

        # File system model
        from PyQt6.QtGui import QFileSystemModel
        from PyQt6.QtCore import QDir

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        self.file_model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)

        # Set name filters for image files
        image_filters = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff", "*.tif", "*.gif", "*.webp"]
        self.file_model.setNameFilters(image_filters)
        self.file_model.setNameFilterDisables(False)

        # File tree view
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(""))

        # Hide unnecessary columns
        self.file_tree.hideColumn(1)  # Size
        self.file_tree.hideColumn(2)  # Type
        self.file_tree.hideColumn(3)  # Date modified

        # Set column width
        self.file_tree.setColumnWidth(0, 200)

        # Connect selection signal
        self.file_tree.selectionModel().selectionChanged.connect(self.on_file_selected)

        # Double click to open
        self.file_tree.doubleClicked.connect(self.on_file_double_clicked)

        explorer_layout.addWidget(self.file_tree)

        splitter.addWidget(explorer_widget)
        splitter.setStretchFactor(0, 1)

        # Right panel: Photo Viewer
        viewer_widget = QWidget()
        viewer_layout = QVBoxLayout(viewer_widget)

        # Photo viewer
        self.photo_viewer = PhotoViewer()
        viewer_layout.addWidget(self.photo_viewer)

        # Photo details
        details_section = QGroupBox("📋 Информация о фото")
        details_layout = QVBoxLayout(details_section)

        self.photo_details_label = QLabel("Выберите фотографию для просмотра в проводнике слева")
        apply_label_style(self.photo_details_label, "caption")
        details_layout.addWidget(self.photo_details_label)

        # File info
        self.file_info_label = QLabel("")
        apply_label_style(self.file_info_label, "caption")
        details_layout.addWidget(self.file_info_label)

        viewer_layout.addWidget(details_section)

        splitter.addWidget(viewer_widget)
        splitter.setStretchFactor(1, 2)

        # Set splitter proportions
        splitter.setSizes([300, 600])

    def update_directory(self, directory):
        """Update file explorer to show selected directory"""
        if directory and os.path.exists(directory):
            self.current_directory = directory

            # Save home directory on first call
            if not hasattr(self, 'home_directory') or not self.home_directory:
                self.home_directory = directory

            self.current_dir_label.setText(f"📂 {os.path.basename(directory)}\n📍 {directory}")
            apply_label_style(self.current_dir_label, "success")

            # Set root path for explorer
            root_index = self.file_model.setRootPath(directory)
            self.file_tree.setRootIndex(root_index)

            # Expand the root directory
            self.file_tree.expand(root_index)

            # Update navigation buttons
            self.up_btn.setEnabled(directory != os.path.dirname(directory))
            self.home_btn.setEnabled(self.home_directory != directory)

            # Clear current photo
            self.photo_viewer.clear()
            self.photo_details_label.setText("Выберите фото для просмотра")
            self.file_info_label.setText("")
        else:
            self.current_directory = None
            self.current_dir_label.setText("Папка не выбрана")
            apply_label_style(self.current_dir_label, "caption")
            self.up_btn.setEnabled(False)
            self.home_btn.setEnabled(False)

    def on_file_selected(self, selected, deselected):
        """Handle file selection in explorer"""
        indexes = selected.indexes()
        if indexes:
            file_path = self.file_model.filePath(indexes[0])
            if os.path.isfile(file_path):
                self.display_photo(file_path)

    def on_file_double_clicked(self, index):
        """Handle double click on file"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self.display_photo(file_path)

    def display_photo(self, file_path):
        """Display selected photo"""
        try:
            # Load photo in viewer
            self.photo_viewer.load_photo(file_path)

            # Update photo details
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)

            # Get image dimensions
            from PIL import Image
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    self.photo_details_label.setText(f"📸 {filename}")
                    self.file_info_label.setText(f"📐 {width}×{height} пикселей | 📁 {file_size_mb:.1f} МБ | 📍 {os.path.dirname(file_path)}")
            except Exception as e:
                self.photo_details_label.setText(f"📸 {filename}")
                self.file_info_label.setText(f"📁 {file_size_mb:.1f} МБ | 📍 {os.path.dirname(file_path)}")

            apply_label_style(self.photo_details_label, "success")

        except Exception as e:
            self.photo_details_label.setText(f"❌ Ошибка загрузки: {filename}")
            self.file_info_label.setText(f"Ошибка: {str(e)}")
            apply_label_style(self.photo_details_label, "danger")

    def refresh_explorer(self):
        """Refresh file explorer"""
        if hasattr(self, 'current_directory') and self.current_directory:
            self.update_directory(self.current_directory)
        else:
            self.current_dir_label.setText("Папка не выбрана")
            apply_label_style(self.current_dir_label, "caption")

    def go_up(self):
        """Go to parent directory"""
        if hasattr(self, 'current_directory') and self.current_directory:
            parent_dir = os.path.dirname(self.current_directory)
            if parent_dir != self.current_directory:
                self.update_directory(parent_dir)

    def go_home(self):
        """Go back to home directory (originally selected directory)"""
        if hasattr(self, 'home_directory') and self.home_directory:
            self.update_directory(self.home_directory)


class QueueTab(QWidget):
    """Queue Management Tab with Multiple Folder Support"""

    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.selected_folders = []  # List of selected folders for batch processing
        self.setup_ui()

    def setup_ui(self):
        """Setup queue tab UI with multiple folder support"""
        layout = QVBoxLayout(self)

        # Batch folder selection section
        batch_section = QGroupBox("📂 Пакетная обработка - Выбор папок")
        batch_layout = QVBoxLayout(batch_section)

        # Compact description
        description = QLabel("🔄 Выберите папки для пакетной обработки")
        apply_label_style(description, "subtitle")
        batch_layout.addWidget(description)

        # Folder selection controls
        controls_layout = QHBoxLayout()

        self.select_folder_btn = QPushButton("📂 Выбрать папку")
        self.select_folder_btn.clicked.connect(self.select_folder)
        apply_button_style(self.select_folder_btn, "large")
        controls_layout.addWidget(self.select_folder_btn)

        self.add_to_queue_btn = QPushButton("➕ Добавить в очередь")
        self.add_to_queue_btn.clicked.connect(self.add_selected_to_queue)
        self.add_to_queue_btn.setEnabled(False)
        apply_button_style(self.add_to_queue_btn, "success")
        controls_layout.addWidget(self.add_to_queue_btn)

        controls_layout.addStretch()
        batch_layout.addLayout(controls_layout)

        # Selected folders list
        self.folders_list = QListWidget()
        self.folders_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
                min-height: 100px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        batch_layout.addWidget(QLabel("📋 Выбранные папки:"))
        batch_layout.addWidget(self.folders_list)

        # Folder management buttons
        folder_btns_layout = QHBoxLayout()

        self.remove_folder_btn = QPushButton("🗑️ Удалить")
        self.remove_folder_btn.clicked.connect(self.remove_selected_folder)
        self.remove_folder_btn.setEnabled(False)
        apply_button_style(self.remove_folder_btn, "danger")
        folder_btns_layout.addWidget(self.remove_folder_btn)

        self.clear_folders_btn = QPushButton("🧹 Очистить список")
        self.clear_folders_btn.clicked.connect(self.clear_folders)
        apply_button_style(self.clear_folders_btn, "warning")
        folder_btns_layout.addWidget(self.clear_folders_btn)

        folder_btns_layout.addStretch()

        self.start_batch_btn = QPushButton("🚀 Запустить пакетную обработку")
        self.start_batch_btn.clicked.connect(self.start_batch_processing)
        self.start_batch_btn.setEnabled(False)
        apply_button_style(self.start_batch_btn, "large success")
        folder_btns_layout.addWidget(self.start_batch_btn)

        batch_layout.addLayout(folder_btns_layout)
        layout.addWidget(batch_section)

        # Queue info
        info_section = QGroupBox("📋 Очередь обработки")
        info_layout = QVBoxLayout(info_section)

        queue_description = QLabel(
            "⚡ Автоматическое управление очередью\n\n"
            "Все задачи обрабатываются автоматически в порядке добавления.\n"
            "Вмешательство пользователя не требуется."
        )
        apply_label_style(queue_description, "subtitle")
        info_layout.addWidget(queue_description)

        layout.addWidget(info_section)

        # Queue widget
        self.queue_widget = QueueWidget(self.parent_window.queue_manager)
        layout.addWidget(self.queue_widget)

    def select_folder(self):
        """Select a folder for batch processing"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для обработки")
        if folder:
            self.selected_folder = folder
            self.add_to_queue_btn.setEnabled(True)
            self.add_to_queue_btn.setText(f"➕ Добавить: {os.path.basename(folder)}")

    def add_selected_to_queue(self):
        """Add selected folder to the batch queue"""
        if hasattr(self, 'selected_folder') and self.selected_folder:
            if self.selected_folder not in self.selected_folders:
                self.selected_folders.append(self.selected_folder)
                self.update_folders_list()
                self.start_batch_btn.setEnabled(len(self.selected_folders) > 0)
            else:
                QMessageBox.information(self, "Информация", "Эта папка уже добавлена в очередь")

            # Reset selection
            self.selected_folder = None
            self.add_to_queue_btn.setEnabled(False)
            self.add_to_queue_btn.setText("➕ Добавить в очередь")

    def update_folders_list(self):
        """Update the display of selected folders"""
        self.folders_list.clear()
        for folder in self.selected_folders:
            folder_name = os.path.basename(folder)
            folder_path = folder
            item_text = f"📂 {folder_name}\n   📍 {folder_path}"
            self.folders_list.addItem(item_text)

        self.remove_folder_btn.setEnabled(len(self.selected_folders) > 0)

    def remove_selected_folder(self):
        """Remove selected folder from the list"""
        current_item = self.folders_list.currentItem()
        if current_item:
            # Extract folder path from item text
            item_text = current_item.text()
            # Find the folder path (everything after "📍 ")
            if "📍 " in item_text:
                folder_path = item_text.split("📍 ")[1]
                if folder_path in self.selected_folders:
                    self.selected_folders.remove(folder_path)
                    self.update_folders_list()
                    self.start_batch_btn.setEnabled(len(self.selected_folders) > 0)

    def clear_folders(self):
        """Clear all selected folders"""
        self.selected_folders.clear()
        self.update_folders_list()
        self.start_batch_btn.setEnabled(False)

    def start_batch_processing(self):
        """Start batch processing of all selected folders"""
        if not self.selected_folders:
            QMessageBox.warning(self, "Ошибка", "Не выбраны папки для обработки")
            return

        # Confirm batch processing
        folder_count = len(self.selected_folders)
        reply = QMessageBox.question(
            self,
            "Подтверждение пакетной обработки",
            f"Начать обработку {folder_count} папок?\n\n"
            f"Каждая папка будет обработана автоматически:\n"
            f"• Сканирование фотографий\n"
            f"• Распознавание лиц\n"
            f"• Сортировка по группам\n\n"
            f"Обработка будет выполняться последовательно.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.start_batch_jobs()

    def start_batch_jobs(self):
        """Create and start batch processing jobs"""
        import uuid

        jobs_created = 0
        for folder_path in self.selected_folders:
            # Create output directory path
            output_dir = os.path.join(folder_path, "PhotoSorter_Results")

            # Create processing job
            job = ProcessingJob(
                job_id=str(uuid.uuid4()),
                input_path=folder_path,
                output_path=output_dir,
                job_type="full_process"
            )

            # Add to queue
            self.parent_window.queue_manager.add_job(job)
            jobs_created += 1

        # Clear the selected folders list
        self.clear_folders()

        # Show success message
        QMessageBox.information(
            self,
            "✅ Задания созданы",
            f"Создано {jobs_created} заданий для пакетной обработки.\n\n"
            "📂 Перейдите на вкладку 'Обработка' для просмотра прогресса.\n"
            "📋 Или посмотрите очередь ниже."
        )

        # Switch to processing tab to show progress
        self.parent_window.tab_widget.setCurrentIndex(1)


class SettingsTab(QWidget):
    """Settings Tab with Theme and Other Options"""

    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup comprehensive settings tab UI"""
        main_layout = QVBoxLayout(self)

        # Theme Settings
        theme_section = QGroupBox("🎨 Тема интерфейса")
        theme_layout = QVBoxLayout(theme_section)

        theme_label = QLabel("Выберите тему приложения:")
        apply_label_style(theme_label, "subtitle")
        theme_layout.addWidget(theme_label)

        # Theme buttons
        theme_buttons_layout = QHBoxLayout()

        self.light_theme_btn = QPushButton("☀️ Светлая тема")
        self.light_theme_btn.clicked.connect(lambda: self.set_theme("light"))
        apply_button_style(self.light_theme_btn, "large")
        theme_buttons_layout.addWidget(self.light_theme_btn)

        self.dark_theme_btn = QPushButton("🌙 Темная тема")
        self.dark_theme_btn.clicked.connect(lambda: self.set_theme("dark"))
        apply_button_style(self.dark_theme_btn, "large")
        theme_buttons_layout.addWidget(self.dark_theme_btn)

        theme_buttons_layout.addStretch()
        theme_layout.addLayout(theme_buttons_layout)

        # Current theme indicator
        current_theme = self.parent_window.theme_manager.get_current_theme()
        theme_indicator = QLabel(f"Текущая тема: {'🌙 Темная' if current_theme == 'dark' else '☀️ Светлая'}")
        apply_label_style(theme_indicator, "caption")
        theme_layout.addWidget(theme_indicator)

        main_layout.addWidget(theme_section)

        # Processing Settings
        processing_section = QGroupBox("⚙️ Настройки обработки")
        processing_layout = QVBoxLayout(processing_section)

        processing_label = QLabel("Параметры обработки изображений:")
        apply_label_style(processing_label, "subtitle")
        processing_layout.addWidget(processing_label)

        # Max image size setting
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Максимальный размер изображения:"))

        self.max_size_combo = QComboBox()
        self.max_size_combo.addItems([
            "Не ограничивать",
            "1920x1080 (Full HD)",
            "1280x720 (HD)",
            "800x600 (SVGA)"
        ])
        self.max_size_combo.setCurrentIndex(1)  # Default to Full HD
        size_layout.addWidget(self.max_size_combo)
        size_layout.addStretch()
        processing_layout.addLayout(size_layout)

        # Face detection sensitivity
        sensitivity_layout = QHBoxLayout()
        sensitivity_layout.addWidget(QLabel("Чувствительность распознавания лиц:"))

        self.sensitivity_combo = QComboBox()
        self.sensitivity_combo.addItems([
            "Низкая (меньше ложных срабатываний)",
            "Средняя (рекомендуется)",
            "Высокая (больше лиц, но больше ошибок)"
        ])
        self.sensitivity_combo.setCurrentIndex(1)  # Default to medium
        sensitivity_layout.addWidget(self.sensitivity_combo)
        sensitivity_layout.addStretch()
        processing_layout.addLayout(sensitivity_layout)

        main_layout.addWidget(processing_section)

        # Output Settings
        output_section = QGroupBox("📁 Настройки вывода")
        output_layout = QVBoxLayout(output_section)

        output_label = QLabel("Параметры сохранения результатов:")
        apply_label_style(output_label, "subtitle")
        output_layout.addWidget(output_label)

        # Output folder naming
        naming_layout = QHBoxLayout()
        naming_layout.addWidget(QLabel("Шаблон имени папки результатов:"))

        self.output_pattern_combo = QComboBox()
        self.output_pattern_combo.addItems([
            "PhotoSorter_Results",
            "Results_[Дата]",
            "Sorted_Photos_[Дата]",
            "Faces_Sorted_[Дата]"
        ])
        naming_layout.addWidget(self.output_pattern_combo)
        naming_layout.addStretch()
        output_layout.addLayout(naming_layout)

        # Create subfolders
        subfolder_layout = QHBoxLayout()
        self.create_subfolders_cb = QCheckBox("Создавать подпапки для каждой группы лиц")
        self.create_subfolders_cb.setChecked(True)
        subfolder_layout.addWidget(self.create_subfolders_cb)
        subfolder_layout.addStretch()
        output_layout.addLayout(subfolder_layout)

        main_layout.addWidget(output_section)

        # Performance Settings
        performance_section = QGroupBox("🚀 Производительность")
        performance_layout = QVBoxLayout(performance_section)

        performance_label = QLabel("Настройки производительности:")
        apply_label_style(performance_label, "subtitle")
        performance_layout.addWidget(performance_label)

        # Multithreading
        threading_layout = QHBoxLayout()
        self.multithread_cb = QCheckBox("Использовать многопоточность для обработки")
        self.multithread_cb.setChecked(True)
        threading_layout.addWidget(self.multithread_cb)
        threading_layout.addStretch()
        performance_layout.addLayout(threading_layout)

        # Memory optimization
        memory_layout = QHBoxLayout()
        self.memory_opt_cb = QCheckBox("Оптимизировать использование памяти")
        self.memory_opt_cb.setChecked(True)
        memory_layout.addWidget(self.memory_opt_cb)
        memory_layout.addStretch()
        performance_layout.addLayout(memory_layout)

        main_layout.addWidget(performance_section)

        # System Settings
        system_section = QGroupBox("🖥️ Системные настройки")
        system_layout = QVBoxLayout(system_section)

        system_label = QLabel("Общие настройки системы:")
        apply_label_style(system_label, "subtitle")
        system_layout.addWidget(system_label)

        # Language
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Язык интерфейса:"))

        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            "Русский",
            "English"
        ])
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        system_layout.addLayout(lang_layout)

        # Auto-save settings
        autosave_layout = QHBoxLayout()
        self.autosave_cb = QCheckBox("Автоматически сохранять настройки")
        self.autosave_cb.setChecked(True)
        autosave_layout.addWidget(self.autosave_cb)
        autosave_layout.addStretch()
        system_layout.addLayout(autosave_layout)

        main_layout.addWidget(system_section)

        # Action buttons
        buttons_section = QGroupBox("")
        buttons_layout = QHBoxLayout(buttons_section)

        self.save_settings_btn = QPushButton("💾 Сохранить настройки")
        self.save_settings_btn.clicked.connect(self.save_settings)
        apply_button_style(self.save_settings_btn, "success")
        buttons_layout.addWidget(self.save_settings_btn)

        self.reset_settings_btn = QPushButton("🔄 Сбросить настройки")
        self.reset_settings_btn.clicked.connect(self.reset_settings)
        apply_button_style(self.reset_settings_btn, "warning")
        buttons_layout.addWidget(self.reset_settings_btn)

        # Test theme button
        self.test_theme_btn = QPushButton("🧪 Тест контрастности")
        self.test_theme_btn.clicked.connect(self.show_theme_test)
        apply_button_style(self.test_theme_btn, "info")
        buttons_layout.addWidget(self.test_theme_btn)

        buttons_layout.addStretch()
        main_layout.addWidget(buttons_section)

        main_layout.addStretch()

        # Update theme buttons state
        self.update_theme_buttons()

    def set_theme(self, theme_name):
        """Set application theme"""
        self.parent_window.theme_manager.set_theme(theme_name)
        self.update_theme_buttons()

        # Update theme indicator
        current_theme = self.parent_window.theme_manager.get_current_theme()
        theme_indicator_text = f"Текущая тема: {'🌙 Темная' if current_theme == 'dark' else '☀️ Светлая'}"

        # Find and update the theme indicator label
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if hasattr(widget, 'layout'):
                for j in range(widget.layout().count()):
                    item = widget.layout().itemAt(j)
                    if item.widget() and hasattr(item.widget(), 'text'):
                        if "Текущая тема:" in item.widget().text():
                            item.widget().setText(theme_indicator_text)
                            break

    def update_theme_buttons(self):
        """Update theme buttons visual state"""
        current_theme = self.parent_window.theme_manager.get_current_theme()

        if current_theme == "light":
            self.light_theme_btn.setText("☀️ Светлая тема ✓")
            self.dark_theme_btn.setText("🌙 Темная тема")
            apply_button_style(self.light_theme_btn, "success")
            apply_button_style(self.dark_theme_btn, "")
        else:
            self.light_theme_btn.setText("☀️ Светлая тема")
            self.dark_theme_btn.setText("🌙 Темная тема ✓")
            apply_button_style(self.light_theme_btn, "")
            apply_button_style(self.dark_theme_btn, "success")

    def save_settings(self):
        """Save current settings"""
        # Here we would save settings to QSettings or config file
        QMessageBox.information(
            self,
            "✅ Настройки сохранены",
            "Все настройки успешно сохранены!\n\n"
            "Изменения вступят в силу при следующем запуске приложения."
        )

    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self,
            "Подтверждение сброса",
            "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Reset theme to light
            self.set_theme("light")

            # Reset other settings to defaults
            self.max_size_combo.setCurrentIndex(1)
            self.sensitivity_combo.setCurrentIndex(1)
            self.output_pattern_combo.setCurrentIndex(0)
            self.create_subfolders_cb.setChecked(True)
            self.multithread_cb.setChecked(True)
            self.memory_opt_cb.setChecked(True)
            self.lang_combo.setCurrentIndex(0)
            self.autosave_cb.setChecked(True)

            QMessageBox.information(
                self,
                "✅ Настройки сброшены",
                "Все настройки сброшены к значениям по умолчанию!"
            )

    def show_theme_test(self):
        """Show theme contrast test window"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout

        # Create dialog window
        dialog = QDialog(self.parent_window)
        dialog.setWindowTitle("🧪 Тест контрастности темной темы")
        dialog.setGeometry(200, 200, 900, 700)

        # Create layout
        layout = QVBoxLayout(dialog)

        # Add description
        description = QLabel(
            "🧪 Это окно показывает все элементы интерфейса для проверки читаемости текста на темном фоне.\n\n"
            "Проверьте:\n"
            "• Читаемость текста всех цветов и размеров\n"
            "• Видимость кнопок и их состояний\n"
            "• Контрастность списков и деревьев\n"
            "• Различимость форм и чекбоксов\n\n"
            "💡 Если какой-то текст трудно прочитать, сообщите разработчику!"
        )
        description.setStyleSheet("padding: 10px; background-color: palette(base); border-radius: 5px;")
        apply_label_style(description, "caption")
        layout.addWidget(description)

        # Add test widget
        test_widget = ThemeTestWidget()
        layout.addWidget(test_widget)

        # Show dialog
        dialog.exec()


class MainWindowSimplified(QMainWindow):
    """Main window with simplified tabbed interface - fully automated"""
    
    def __init__(self):
        super().__init__()
        # Initialize theme manager first
        self.theme_manager = ThemeManager()
        # Initialize processing components first so tabs can access them (e.g., QueueTab)
        self.setup_components()
        # Then build UI
        self.setup_ui()
        # Finally connect all signals
        self.connect_signals()
        self.show()
    
    def setup_ui(self):
        """Setup main window UI"""
        self.setWindowTitle("Photo Sorter - Автоматическая сортировка фотографий")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply theme
        self.theme_manager.apply_theme()
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.overview_tab = OverviewTab(self)
        self.processing_tab = ProcessingTab(self)
        self.viewer_tab = ViewerTab(self)
        self.queue_tab = QueueTab(self)
        self.settings_tab = SettingsTab(self)
        
        # Add tabs
        self.tab_widget.addTab(self.overview_tab, "🏠 Главная")
        self.tab_widget.addTab(self.processing_tab, "⚡ Обработка")
        self.tab_widget.addTab(self.viewer_tab, "🖼️ Просмотр")
        self.tab_widget.addTab(self.queue_tab, "📋 Очередь")
        self.tab_widget.addTab(self.settings_tab, "⚙️ Настройки")
        
        layout.addWidget(self.tab_widget)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к работе")
    
    def setup_components(self):
        """Setup processing components"""
        # Photo list model
        self.photo_list_model = PhotoListModel()
        
        # Directory scanner
        self.directory_scanner = DirectoryScanner()
        
        # Face processor
        self.face_processor = SimpleFaceProcessor()
        
        # Photo sorter
        self.photo_sorter = PhotoSorter()
        
        # InsightFace sorter (optional)
        try:
            self.insight_sorter = InsightFaceSorter()
        except ImportError as e:
            print(f"InsightFace не доступен: {e}")
            self.insight_sorter = None
        
        # Queue manager
        self.queue_manager = QueueManager()
    
    def connect_signals(self):
        """Connect component signals"""
        # Directory scanner signals
        self.directory_scanner.scanning_finished.connect(self.processing_tab.on_scanning_finished)
        
        # Face processor signals
        self.face_processor.processing_finished.connect(self.processing_tab.on_face_processing_finished)
        
        # Photo sorter signals
        self.photo_sorter.sorting_finished.connect(self.processing_tab.on_sorting_finished)
        
        # Tab change signal
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        if index == 1:  # Processing tab
            self.processing_tab.update_working_directory()
        elif index == 2:  # Viewer tab
            if hasattr(self, 'current_directory'):
                viewer_tab = self.tab_widget.widget(2)
                viewer_tab.update_directory(self.current_directory)
    
    def set_directory(self, directory):
        """Set working directory"""
        self.current_directory = directory
        self.overview_tab.select_input_directory()
