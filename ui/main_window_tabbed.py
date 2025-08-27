"""
Main Window with Tabbed Interface for Photo Sorting Application
Divided into logical pages for better user experience
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeView, QListView, QLabel, QPushButton, QProgressBar,
    QStatusBar, QMenuBar, QMenu, QFileDialog, QMessageBox,
    QGroupBox, QGridLayout, QScrollArea, QLineEdit, QTabWidget
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


class OverviewTab(QWidget):
    """Overview and Quick Start Tab"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup overview tab UI"""
        layout = QVBoxLayout(self)
        
        # Welcome section
        welcome_section = QGroupBox("🏠 Добро пожаловать в Photo Sorter")
        welcome_layout = QVBoxLayout(welcome_section)
        
        title = QLabel("Умная сортировка фотографий по людям")
        apply_label_style(title, "title")
        welcome_layout.addWidget(title)
        
        description = QLabel(
            "🖼️ Умная сортировка фотографий по людям\n\n"
            "Программа автоматически:\n"
            "• Найдет все фотографии в выбранной папке\n"
            "• Распознает лица на изображениях\n"
            "• Сгруппирует фото по людям\n"
            "• Создаст папки с результатами\n\n"
            "Всего 3 простых шага!"
        )
        apply_label_style(description, "subtitle")
        welcome_layout.addWidget(description)
        
        layout.addWidget(welcome_section)
        
        # Quick start section
        quick_section = QGroupBox("🚀 Быстрый старт")
        quick_layout = QVBoxLayout(quick_section)
        
        # Step 1
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
        
        # Step 2 (автоматически)
        step2_layout = QHBoxLayout()
        step2_num = QLabel("2️⃣")
        step2_num.setFixedWidth(40)
        step2_layout.addWidget(step2_num)

        step2_text = QLabel("📤 Папка результатов: будет создана автоматически")
        apply_label_style(step2_text, "caption")
        step2_layout.addWidget(step2_text)

        self.output_path_label = QLabel("Входная_папка/PhotoSorter_Results")
        apply_label_style(self.output_path_label, "success")
        step2_layout.addWidget(self.output_path_label)

        quick_layout.addLayout(step2_layout)
        
        # Step 3
        step3_layout = QHBoxLayout()
        step3_num = QLabel("3️⃣")
        step3_num.setFixedWidth(40)
        step3_layout.addWidget(step3_num)
        
        self.start_btn = QPushButton("🎬 СТАРТ - Начать сортировку!")
        self.start_btn.clicked.connect(self.start_processing)
        self.start_btn.setEnabled(False)
        apply_button_style(self.start_btn, "large success")
        step3_layout.addWidget(self.start_btn)
        
        quick_layout.addLayout(step3_layout)
        
        layout.addWidget(quick_section)
        

        
        # Status section
        status_section = QGroupBox("📊 Статус")
        status_layout = QVBoxLayout(status_section)
        
        self.status_label = QLabel("Готов к работе")
        apply_label_style(self.status_label, "subtitle")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_section)
        layout.addStretch()
    
    def cancel_operation(self):
        """Cancel current operation"""
        processing_tab = self.parent_window.tab_widget.widget(1)
        processing_tab.cancel_operation()
        
        # Сбрасываем интерфейс
        self.progress_section.setVisible(False)
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🎬 СТАРТ - Начать сортировку!")
        self.status_label.setText("❌ Обработка отменена")
    
    def on_processing_finished(self, success=True):
        """Called when processing is finished"""
        self.progress_section.setVisible(False)
        self.start_btn.setEnabled(True)
        self.start_btn.setText("🎬 СТАРТ - Начать сортировку!")
        
        if success:
            self.status_label.setText("✅ Обработка завершена успешно! Проверьте папку PhotoSorter_Results.")
        else:
            self.status_label.setText("❌ Обработка прервана или завершилась с ошибкой")
    
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
            self.output_path_label.setText(f"{os.path.basename(directory)}/PhotoSorter_Results")
            apply_label_style(self.output_path_label, "success")

            # Активируем кнопку СТАРТ
            self.start_btn.setEnabled(True)
            self.status_label.setText(f"✅ Готово к обработке! Нажмите СТАРТ для начала.")
    
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
                self.status_label.setText("⚡ Обработка запущена! Перейдите на вкладку 'Обработка' для просмотра прогресса.")
                
                # Переключаемся на вкладку Processing
                self.parent_window.tab_widget.setCurrentIndex(1)
                
                # Запускаем полную обработку
                processing_tab = self.parent_window.tab_widget.widget(1)
                processing_tab.start_full_processing(input_dir, output_dir)
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите папку с фотографиями!")


class ProcessingTab(QWidget):
    """Processing and Manual Control Tab"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup processing tab UI"""
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
        
        current_layout.addLayout(controls_layout)
        layout.addWidget(current_section)
        
        # Progress Display (показывает только прогресс)
        progress_display_section = QGroupBox("📊 Текущий прогресс")
        progress_display_layout = QVBoxLayout(progress_display_section)
        
        # Directory info
        dir_info_layout = QHBoxLayout()
        dir_info_layout.addWidget(QLabel("📁 Рабочая папка:"))
        self.working_dir_label = QLabel("Не выбрана")
        apply_label_style(self.working_dir_label, "caption")
        dir_info_layout.addWidget(self.working_dir_label)
        dir_info_layout.addStretch()
        progress_display_layout.addLayout(dir_info_layout)
        
        # Auto progress info
        auto_info = QLabel("⚡ Полностью автоматический процесс - управление не требуется")
        apply_label_style(auto_info, "subtitle")
        progress_display_layout.addWidget(auto_info)
        
        layout.addWidget(progress_display_section)
        
        # Results section
        results_section = QGroupBox("📊 Результаты")
        results_layout = QVBoxLayout(results_section)
        
        self.results_label = QLabel("Обработка не запускалась")
        apply_label_style(self.results_label, "caption")
        results_layout.addWidget(self.results_label)
        
        layout.addWidget(results_section)
        layout.addStretch()
    
    def update_working_directory(self):
        """Update working directory display"""
        if hasattr(self.parent_window, 'current_directory'):
            input_dir = self.parent_window.current_directory
            output_dir = os.path.join(input_dir, "PhotoSorter_Results")
            self.working_dir_label.setText(f"{os.path.basename(input_dir)} → PhotoSorter_Results")
            apply_label_style(self.working_dir_label, "success")
            self.scan_btn.setEnabled(True)
        else:
            self.working_dir_label.setText("Не выбрана")
            apply_label_style(self.working_dir_label, "caption")
    
    def start_full_processing(self):
        """Start full automated processing"""
        if not hasattr(self.parent_window, 'current_directory'):
            return

        # Создаем выходную папку автоматически
        input_dir = self.parent_window.current_directory
        output_dir = os.path.join(input_dir, "PhotoSorter_Results")

        # Создаем папку, если она не существует
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать папку результатов: {e}")
            return

        self.parent_window.output_directory = output_dir

        # Create job and add to queue
        import uuid
        job = ProcessingJob(
            job_id=str(uuid.uuid4()),
            input_path=input_dir,
            output_path=output_dir,
            job_type="full_process"
        )

        self.parent_window.queue_manager.add_job(job)
        self.current_operation_label.setText("🚀 Полная обработка запущена")
        self.working_dir_label.setText(f"{os.path.basename(input_dir)} → PhotoSorter_Results")

        # Show success message
        QMessageBox.information(
            self, "✅ Обработка запущена",
            f"Полная обработка фотографий запущена!\n\n"
            f"📂 Входная папка: {os.path.basename(input_dir)}\n"
            f"📤 Результаты: {os.path.basename(output_dir)}\n\n"
            f"Процесс:\n"
            f"• 🔍 Сканирование фото\n"
            f"• 👤 Распознавание лиц\n"
            f"• 📋 Группировка\n"
            f"• 📁 Создание папок\n\n"
            f"Следите за прогрессом на этой вкладке!"
        )
        
    def start_scanning(self):
        """Start scanning"""
        self.current_operation_label.setText("🔍 Сканирование...")
        self.scan_status.setText("В процессе...")
        apply_label_style(self.scan_status, "warning")
        
    def start_face_detection(self):
        """Start face detection"""
        self.current_operation_label.setText("👤 Поиск лиц...")
        self.detect_status.setText("В процессе...")
        apply_label_style(self.detect_status, "warning")
        
    def start_sorting(self):
        """Start sorting"""
        self.current_operation_label.setText("📋 Сортировка...")
        self.sort_status.setText("В процессе...")
        apply_label_style(self.sort_status, "warning")
        
    def cancel_operation(self):
        """Cancel current operation"""
        self.current_operation_label.setText("⏹️ Операция отменена")


class BrowseTab(QWidget):
    """Browse Photos and Results Tab"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup browse tab UI"""
        layout = QHBoxLayout(self)
        
        # Left panel - photo list
        left_panel = QGroupBox("🖼️ Фотографии")
        left_layout = QVBoxLayout(left_panel)
        
        self.photo_list = QListView()
        self.photo_list.setModel(self.parent_window.photo_model)
        self.photo_list.clicked.connect(self.on_photo_selected)
        left_layout.addWidget(self.photo_list)
        
        layout.addWidget(left_panel)
        
        # Right panel - photo viewer and info
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Photo viewer
        viewer_section = QGroupBox("🖼️ Предварительный просмотр")
        viewer_layout = QVBoxLayout(viewer_section)
        viewer_layout.addWidget(self.parent_window.photo_viewer)
        right_layout.addWidget(viewer_section)
        
        # Photo info
        info_section = QGroupBox("📋 Информация")
        info_layout = QGridLayout(info_section)
        
        self.filename_label = QLabel("-")
        self.size_label = QLabel("-")
        self.faces_label = QLabel("-")
        
        info_layout.addWidget(QLabel("📄 Файл:"), 0, 0)
        info_layout.addWidget(self.filename_label, 0, 1)
        info_layout.addWidget(QLabel("📏 Размер:"), 1, 0)
        info_layout.addWidget(self.size_label, 1, 1)
        info_layout.addWidget(QLabel("👤 Лица:"), 2, 0)
        info_layout.addWidget(self.faces_label, 2, 1)
        
        right_layout.addWidget(info_section)
        layout.addWidget(right_panel)
    
    def on_photo_selected(self, index):
        """Handle photo selection"""
        photo_path = self.parent_window.photo_model.get_photo_path(index.row())
        if photo_path:
            self.parent_window.photo_viewer.load_photo(photo_path)
            self.update_photo_info(photo_path)
    
    def update_photo_info(self, photo_path):
        """Update photo information"""
        filename = os.path.basename(photo_path)
        size_bytes = os.path.getsize(photo_path)
        size_mb = size_bytes / (1024 * 1024)
        size_text = f"{size_mb:.1f} МБ" if size_mb >= 1 else f"{size_bytes / 1024:.1f} КБ"
        
        self.filename_label.setText(filename)
        self.size_label.setText(size_text)
        self.faces_label.setText("0")


class QueueTab(QWidget):
    """Queue Management Tab"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup queue tab UI"""
        layout = QVBoxLayout(self)
        
        # Queue widget
        self.queue_widget = QueueWidget(self.parent_window.queue_manager)
        layout.addWidget(self.queue_widget)


class SettingsTab(QWidget):
    """Settings and Advanced Options Tab"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup settings tab UI"""
        layout = QVBoxLayout(self)
        
        # Processing settings
        processing_section = QGroupBox("⚙️ Настройки обработки")
        processing_layout = QVBoxLayout(processing_section)
        
        # InsightFace status
        insight_status = "✅ Доступен" if self.parent_window.insight_sorter else "❌ Недоступен"
        insight_label = QLabel(f"🧠 InsightFace: {insight_status}")
        apply_label_style(insight_label, "success" if self.parent_window.insight_sorter else "danger")
        processing_layout.addWidget(insight_label)
        
        if not self.parent_window.insight_sorter:
            install_label = QLabel("💡 Для установки: pip install insightface onnxruntime")
            apply_label_style(install_label, "caption")
            processing_layout.addWidget(install_label)
        
        layout.addWidget(processing_section)
        
        # About section
        about_section = QGroupBox("ℹ️ О программе")
        about_layout = QVBoxLayout(about_section)
        
        about_text = QLabel(
            "Photo Sorter v2.0\n"
            "Умная сортировка фотографий по людям\n\n"
            "Использует:\n"
            "• OpenCV для базового распознавания лиц\n"
            "• InsightFace для точного распознавания (опционально)\n"
            "• PyQt6 для современного интерфейса"
        )
        apply_label_style(about_text, "caption")
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_section)
        layout.addStretch()


class MainWindowTabbed(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        self.init_components()
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
    
    def init_components(self):
        """Initialize all components"""
        self.setWindowTitle("🖼️ Photo Sorter - Умная сортировка фотографий")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(MODERN_STYLESHEET)
        
        # Initialize core components
        self.photo_viewer = PhotoViewer()
        self.directory_scanner = DirectoryScanner()
        self.face_processor = SimpleFaceProcessor()
        self.photo_sorter = PhotoSorter()
        self.photo_model = PhotoListModel()
        self.queue_manager = QueueManager()
        
        # Initialize InsightFace if available
        try:
            self.insight_sorter = InsightFaceSorter()
        except Exception:
            self.insight_sorter = None
    
    def setup_ui(self):
        """Setup the tabbed user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.overview_tab = OverviewTab(self)
        self.processing_tab = ProcessingTab(self)
        self.browse_tab = BrowseTab(self)
        self.queue_tab = QueueTab(self)
        self.settings_tab = SettingsTab(self)
        
        # Add tabs
        self.tab_widget.addTab(self.overview_tab, "🏠 Обзор")
        self.tab_widget.addTab(self.processing_tab, "⚙️ Обработка")
        self.tab_widget.addTab(self.browse_tab, "🖼️ Просмотр")
        self.tab_widget.addTab(self.queue_tab, "⏳ Очередь")
        self.tab_widget.addTab(self.settings_tab, "🔧 Настройки")
        
        # Connect tab change
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        layout.addWidget(self.tab_widget)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("Файл")
        
        open_action = QAction("Открыть папку...", self)
        open_action.triggered.connect(self.overview_tab.select_input_directory)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("Вид")
        
        for i, (name, _) in enumerate([
            ("Обзор", "🏠"),
            ("Обработка", "⚙️"),
            ("Просмотр", "🖼️"),
            ("Очередь", "⏳"),
            ("Настройки", "🔧")
        ]):
            action = QAction(f"{name}", self)
            action.triggered.connect(lambda checked, idx=i: self.tab_widget.setCurrentIndex(idx))
            view_menu.addAction(action)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = self.statusBar()
        self.status_label = QLabel("Готов к работе")
        self.status_bar.addWidget(self.status_label)
    
    def on_tab_changed(self, index):
        """Handle tab change"""
        tab_names = ["Обзор", "Обработка", "Просмотр", "Очередь", "Настройки"]
        if index < len(tab_names):
            self.status_label.setText(f"Открыта вкладка: {tab_names[index]}")
        
        # Update processing tab when switched to
        if index == 1:  # Processing tab
            self.processing_tab.update_working_directory()
