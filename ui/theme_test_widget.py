"""
Theme Test Widget for checking contrast and readability
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QListWidget, QTreeWidget, QTreeWidgetItem,
    QComboBox, QCheckBox, QLineEdit, QTextEdit, QProgressBar,
    QTabWidget, QSplitter
)
from PyQt6.QtCore import Qt


class ThemeTestWidget(QWidget):
    """Widget for testing theme contrast and readability"""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup test interface with all UI elements"""
        main_layout = QVBoxLayout(self)

        # Header
        header = QLabel("🧪 Тестирование контрастности темной темы")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(header)

        # Create splitter for organized layout
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel: Controls and Forms
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Right panel: Lists and Trees
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        main_layout.addWidget(splitter)

        # Bottom panel: Status and Progress
        bottom_panel = self.create_bottom_panel()
        main_layout.addWidget(bottom_panel)

        # Set splitter proportions
        splitter.setSizes([400, 400])

    def create_left_panel(self):
        """Create left panel with buttons, forms, and controls"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Buttons section
        buttons_group = QGroupBox("🎛️ Кнопки")
        buttons_layout = QVBoxLayout(buttons_group)

        # Regular buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Обычная кнопка"))
        btn_layout.addWidget(QPushButton("🌙 Темная тема"))
        btn_layout.addWidget(QPushButton("☀️ Светлая тема"))
        buttons_layout.addLayout(btn_layout)

        # Styled buttons
        styled_layout = QHBoxLayout()
        success_btn = QPushButton("✅ Успех")
        success_btn.setProperty("class", "success")
        danger_btn = QPushButton("❌ Ошибка")
        danger_btn.setProperty("class", "danger")
        warning_btn = QPushButton("⚠️ Предупреждение")
        warning_btn.setProperty("class", "warning")

        styled_layout.addWidget(success_btn)
        styled_layout.addWidget(danger_btn)
        styled_layout.addWidget(warning_btn)
        buttons_layout.addLayout(styled_layout)

        # Disabled button
        disabled_btn = QPushButton("🚫 Отключена")
        disabled_btn.setEnabled(False)
        buttons_layout.addWidget(disabled_btn)

        layout.addWidget(buttons_group)

        # Forms section
        forms_group = QGroupBox("📝 Формы")
        forms_layout = QVBoxLayout(forms_group)

        # Text input
        forms_layout.addWidget(QLabel("Текстовое поле:"))
        text_input = QLineEdit()
        text_input.setPlaceholderText("Введите текст для проверки читаемости...")
        forms_layout.addWidget(text_input)

        # Combo box
        forms_layout.addWidget(QLabel("Выпадающий список:"))
        combo = QComboBox()
        combo.addItems([
            "Обычный текст",
            "Длинный текст для проверки обрезки",
            "Текст с эмодзи 🎨 🌙",
            "Числа и символы: 123!@#"
        ])
        forms_layout.addWidget(combo)

        # Checkboxes
        forms_layout.addWidget(QLabel("Чекбоксы:"))
        forms_layout.addWidget(QCheckBox("Включить оптимизацию"))
        forms_layout.addWidget(QCheckBox("Использовать многопоточность"))
        forms_layout.addWidget(QCheckBox("Показывать прогресс"))

        layout.addWidget(forms_group)

        # Text section
        text_group = QGroupBox("📄 Текст")
        text_layout = QVBoxLayout(text_group)

        # Different text styles
        text_layout.addWidget(QLabel("Обычный текст"))
        text_layout.addWidget(QLabel("Полужирный текст").setStyleSheet("font-weight: bold;"))
        text_layout.addWidget(QLabel("Курсивный текст").setStyleSheet("font-style: italic;"))

        # Status labels
        status_layout = QVBoxLayout()
        status_layout.addWidget(QLabel("Статус: ✅ Готово"))
        status_layout.addWidget(QLabel("Предупреждение: ⚠️ Проверьте настройки"))
        status_layout.addWidget(QLabel("Ошибка: ❌ Файл не найден"))

        text_layout.addLayout(status_layout)

        layout.addWidget(text_group)

        layout.addStretch()
        return panel

    def create_right_panel(self):
        """Create right panel with lists and trees"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # List section
        list_group = QGroupBox("📋 Списки")
        list_layout = QVBoxLayout(list_group)

        # Simple list
        list_layout.addWidget(QLabel("Простой список:"))
        simple_list = QListWidget()
        simple_list.addItems([
            "Элемент списка 1",
            "Элемент списка 2 с длинным текстом",
            "Элемент списка 3 🎨",
            "Элемент списка 4 (выбранный)",
            "Элемент списка 5"
        ])
        # Select one item for testing
        simple_list.setCurrentRow(3)
        list_layout.addWidget(simple_list)

        layout.addWidget(list_group)

        # Tree section
        tree_group = QGroupBox("🌳 Дерево")
        tree_layout = QVBoxLayout(tree_group)

        tree_layout.addWidget(QLabel("Дерево файлов:"))
        tree = QTreeWidget()
        tree.setHeaderLabel("Файловая структура")

        # Create tree structure
        root = QTreeWidgetItem(tree)
        root.setText(0, "📁 PhotoSorter_Project")

        src_folder = QTreeWidgetItem(root)
        src_folder.setText(0, "📁 src")

        ui_folder = QTreeWidgetItem(src_folder)
        ui_folder.setText(0, "📁 ui")

        files = ["main_window_simplified.py", "theme_manager.py", "photo_viewer.py"]
        for file in files:
            file_item = QTreeWidgetItem(ui_folder)
            file_item.setText(0, f"📄 {file}")

        tree.expandAll()
        tree_layout.addWidget(tree)

        layout.addWidget(tree_group)

        layout.addStretch()
        return panel

    def create_bottom_panel(self):
        """Create bottom panel with progress and tabs"""
        panel = QWidget()
        layout = QHBoxLayout(panel)

        # Progress section
        progress_group = QGroupBox("📊 Прогресс")
        progress_layout = QVBoxLayout(progress_group)

        progress_layout.addWidget(QLabel("Сканирование файлов:"))
        progress_bar = QProgressBar()
        progress_bar.setValue(75)
        progress_layout.addWidget(progress_bar)

        progress_layout.addWidget(QLabel("Обработка изображений:"))
        progress_bar2 = QProgressBar()
        progress_bar2.setValue(45)
        progress_layout.addWidget(progress_bar2)

        layout.addWidget(progress_group)

        # Tab section
        tab_group = QGroupBox("📑 Вкладки")
        tab_layout = QVBoxLayout(tab_group)

        tabs = QTabWidget()
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("🏠 Главная - Контент первой вкладки"))
        tab1_layout.addWidget(QPushButton("Кнопка на первой вкладке"))

        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("⚙️ Настройки - Контент второй вкладки"))
        tab2_layout.addWidget(QComboBox())
        tab2_layout.addWidget(QCheckBox("Тестовый чекбокс"))

        tabs.addTab(tab1, "🏠 Главная")
        tabs.addTab(tab2, "⚙️ Настройки")

        tab_layout.addWidget(tabs)

        layout.addWidget(tab_group)

        return panel
