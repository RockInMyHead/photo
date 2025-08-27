"""
Theme Manager for Photo Sorter Application
Handles light/dark theme switching and customization
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings


class ThemeManager:
    """Manages application themes and styles"""

    # Light theme colors
    LIGHT_THEME = {
        'primary': '#3498db',
        'primary_dark': '#2980b9',
        'secondary': '#2ecc71',
        'secondary_dark': '#27ae60',
        'danger': '#e74c3c',
        'danger_dark': '#c0392b',
        'warning': '#f39c12',
        'warning_dark': '#e67e22',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'background': '#ffffff',
        'surface': '#f5f6fa',
        'border': '#dee2e6',
        'text': '#2c3e50',
        'text_secondary': '#6c757d',
        'success': '#28a745'
    }

    # Dark theme colors - High contrast for better readability
    DARK_THEME = {
        'primary': '#6bb6ff',        # Более яркий синий для лучшей видимости
        'primary_dark': '#4a9eff',   # Темнее, но контрастный
        'secondary': '#4ade80',      # Более яркий зеленый
        'secondary_dark': '#22c55e', # Яркий зеленый для акцента
        'danger': '#ff6b6b',         # Более яркий красный
        'danger_dark': '#ff5252',    # Яркий красный для ошибок
        'warning': '#ffd93d',        # Более яркий желтый
        'warning_dark': '#ffc107',   # Яркий оранжевый
        'info': '#6bb6ff',          # Синий для информации
        'light': '#374151',         # Темно-серый для светлых элементов
        'dark': '#ffffff',          # Белый текст на темном фоне
        'background': '#0f172a',     # Темно-синий фон (лучше чем черный)
        'surface': '#1e293b',       # Светлее фона для поверхностей
        'border': '#475569',        # Серо-голубой для границ
        'text': '#f1f5f9',          # Почти белый для основного текста
        'text_secondary': '#cbd5e1', # Светло-серый для второстепенного текста
        'success': '#4ade80'        # Яркий зеленый для успеха
    }

    def __init__(self):
        self.settings = QSettings("PhotoSorter", "Theme")
        self.current_theme = self.settings.value("theme", "light")

    def get_theme_colors(self):
        """Get current theme colors"""
        if self.current_theme == "dark":
            return self.DARK_THEME
        return self.LIGHT_THEME

    def set_theme(self, theme_name):
        """Set application theme"""
        self.current_theme = theme_name
        self.settings.setValue("theme", theme_name)
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to application"""
        colors = self.get_theme_colors()

        # Generate stylesheet with current colors
        stylesheet = self.generate_stylesheet(colors)

        # Apply to all widgets
        if QApplication.instance():
            QApplication.instance().setStyleSheet(stylesheet)

    def generate_stylesheet(self, colors):
        """Generate stylesheet with given colors"""
        return f"""
        /* Main Application */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text']};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 9pt;
        }}

        /* Group Boxes */
        QGroupBox {{
            font-weight: bold;
            font-size: 10pt;
            color: {colors['text']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            margin-top: 1ex;
            padding-top: 10px;
            background-color: {colors['surface']};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background-color: {colors['background']};
            border-radius: 4px;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {colors['primary']};
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            font-size: 9pt;
            font-weight: 500;
            border-radius: 6px;
            min-height: 20px;
            min-width: 80px;
        }}

        QPushButton:hover {{
            background-color: {colors['primary_dark']};
        }}

        QPushButton:pressed {{
            background-color: {colors['primary_dark']};
        }}

        QPushButton:disabled {{
            background-color: {colors['border']};
            color: {colors['text_secondary']};
        }}

        /* Success button variant */
        QPushButton[class="success"] {{
            background-color: {colors['secondary']};
        }}

        QPushButton[class="success"]:hover {{
            background-color: {colors['secondary_dark']};
        }}

        /* Danger button variant */
        QPushButton[class="danger"] {{
            background-color: {colors['danger']};
        }}

        QPushButton[class="danger"]:hover {{
            background-color: {colors['danger_dark']};
        }}

        /* Warning button variant */
        QPushButton[class="warning"] {{
            background-color: {colors['warning']};
        }}

        QPushButton[class="warning"]:hover {{
            background-color: {colors['warning_dark']};
        }}

        /* Large button variant */
        QPushButton[class="large"] {{
            padding: 15px 30px;
            font-size: 12pt;
            font-weight: bold;
            min-height: 30px;
            border-radius: 8px;
        }}

        /* Text inputs */
        QLineEdit {{
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 9pt;
            background-color: {colors['background']};
            color: {colors['text']};
        }}

        QLineEdit:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}

        QLineEdit:disabled {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
        }}

        /* Progress bars */
        QProgressBar {{
            border: 2px solid {colors['border']};
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            background-color: {colors['surface']};
            color: {colors['text']};
            min-height: 20px;
        }}

        QProgressBar::chunk {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 {colors['primary']},
                                stop: 1 {colors['primary_dark']});
            border-radius: 6px;
            margin: 2px;
        }}

        /* Lists */
        QListView, QListWidget {{
            border: 1px solid {colors['border']};
            border-radius: 6px;
            background-color: {colors['background']};
            alternate-background-color: {colors['surface']};
            selection-background-color: {colors['primary']};
            selection-color: {colors['dark']};
            outline: none;
            color: {colors['text']};
        }}

        QListView::item, QListWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {colors['border']};
            color: {colors['text']};
        }}

        QListView::item:hover, QListWidget::item:hover {{
            background-color: {colors['surface']};
            color: {colors['text']};
        }}

        QListView::item:selected, QListWidget::item:selected {{
            background-color: {colors['primary']};
            color: {colors['dark']};
        }}

        /* Tree views */
        QTreeView {{
            border: 1px solid {colors['border']};
            border-radius: 6px;
            background-color: {colors['background']};
            alternate-background-color: {colors['surface']};
            selection-background-color: {colors['primary']};
            selection-color: {colors['dark']};
            outline: none;
            color: {colors['text']};
        }}

        QTreeView::item {{
            padding: 4px;
            border-bottom: 1px solid {colors['border']};
            color: {colors['text']};
        }}

        QTreeView::item:hover {{
            background-color: {colors['surface']};
            color: {colors['text']};
        }}

        QTreeView::item:selected {{
            background-color: {colors['primary']};
            color: {colors['dark']};
        }}

        /* Combo boxes */
        QComboBox {{
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 4px 8px;
            background-color: {colors['background']};
            color: {colors['text']};
            min-width: 100px;
        }}

        QComboBox:hover {{
            border-color: {colors['primary']};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid {colors['text']};
            margin-right: 5px;
        }}

        QComboBox QListView {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 1px solid {colors['border']};
        }}

        /* Checkboxes */
        QCheckBox {{
            color: {colors['text']};
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {colors['border']};
            border-radius: 3px;
            background-color: {colors['background']};
        }}

        QCheckBox::indicator:hover {{
            border-color: {colors['primary']};
        }}

        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQgOEwxMCA0IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
        }}

        /* Scroll areas */
        QScrollArea {{
            border: 1px solid {colors['border']};
            border-radius: 6px;
            background-color: {colors['background']};
        }}

        /* Status bar */
        QStatusBar {{
            background-color: {colors['surface']};
            border-top: 1px solid {colors['border']};
            color: {colors['text']};
            font-size: 8pt;
        }}

        /* Tab widget */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            background-color: {colors['background']};
        }}

        QTabBar::tab {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            padding: 8px 16px;
            margin-right: 2px;
            border-radius: 6px 6px 0 0;
            color: {colors['text_secondary']};
        }}

        QTabBar::tab:selected {{
            background-color: {colors['background']};
            border-bottom: 2px solid {colors['primary']};
            color: {colors['text']};
            font-weight: bold;
        }}

        QTabBar::tab:hover {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}

        /* Labels */
        QLabel {{
            color: {colors['text']};
            font-size: 9pt;
        }}

        QLabel[class="title"] {{
            font-size: 14pt;
            font-weight: bold;
            color: {colors['text']};
            margin: 10px 0;
        }}

        QLabel[class="subtitle"] {{
            font-size: 11pt;
            font-weight: 500;
            color: {colors['text']};
            margin: 5px 0;
        }}

        QLabel[class="caption"] {{
            font-size: 8pt;
            color: {colors['text_secondary']};
        }}

        QLabel[class="success"] {{
            color: {colors['success']};
            font-weight: bold;
        }}

        QLabel[class="danger"] {{
            color: {colors['danger']};
            font-weight: bold;
        }}

        QLabel[class="warning"] {{
            color: {colors['warning']};
            font-weight: bold;
        }}

        /* Improved disabled button visibility in dark theme */
        QPushButton:disabled {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
            border: 1px solid {colors['border']};
        }}

        /* Better hover effects for dark theme */
        QPushButton:hover {{
            background-color: {colors['primary_dark']};
            border: 1px solid {colors['primary']};
        }}

        QPushButton:pressed {{
            background-color: {colors['primary_dark']};
            border: 1px solid {colors['primary_dark']};
        }}

        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {colors['surface']};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {colors['border']};
            min-height: 20px;
            border-radius: 6px;
            margin: 2px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {colors['text_secondary']};
        }}
        """

    def get_current_theme(self):
        """Get current theme name"""
        return self.current_theme

    def is_dark_theme(self):
        """Check if dark theme is active"""
        return self.current_theme == "dark"

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme(new_theme)
