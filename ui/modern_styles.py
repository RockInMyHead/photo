"""
Modern UI styles for Photo Sorter application
"""

# Modern color palette
COLORS = {
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

# Modern stylesheet for the application - Qt compatible
MODERN_STYLESHEET = f"""
/* Main Application */
QMainWindow {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 9pt;
}}

/* Group Boxes */
QGroupBox {{
    font-weight: bold;
    font-size: 10pt;
    color: {COLORS['text']};
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 1ex;
    padding-top: 10px;
    background-color: {COLORS['surface']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 8px 0 8px;
    background-color: {COLORS['background']};
    border-radius: 4px;
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS['primary']};
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
    background-color: {COLORS['primary_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

/* Success button variant */
QPushButton[class="success"] {{
    background-color: {COLORS['secondary']};
}}

QPushButton[class="success"]:hover {{
    background-color: {COLORS['secondary_dark']};
}}

/* Danger button variant */
QPushButton[class="danger"] {{
    background-color: {COLORS['danger']};
}}

QPushButton[class="danger"]:hover {{
    background-color: {COLORS['danger_dark']};
}}

/* Warning button variant */
QPushButton[class="warning"] {{
    background-color: {COLORS['warning']};
}}

QPushButton[class="warning"]:hover {{
    background-color: {COLORS['warning_dark']};
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
    border: 2px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 9pt;
    background-color: {COLORS['background']};
}}

QLineEdit:focus {{
    border-color: {COLORS['primary']};
    outline: none;
}}

QLineEdit:disabled {{
    background-color: {COLORS['surface']};
    color: {COLORS['text_secondary']};
}}

/* Progress bars */
QProgressBar {{
    border: 2px solid {COLORS['border']};
    border-radius: 8px;
    text-align: center;
    font-weight: bold;
    background-color: {COLORS['surface']};
    color: {COLORS['text']};
    min-height: 20px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                stop: 0 {COLORS['primary']},
                                stop: 1 {COLORS['primary_dark']});
    border-radius: 6px;
    margin: 2px;
}}

/* Lists */
QListView, QListWidget {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background-color: {COLORS['background']};
    alternate-background-color: {COLORS['surface']};
    selection-background-color: {COLORS['primary']};
    selection-color: white;
    outline: none;
}}

QListView::item, QListWidget::item {{
    padding: 8px;
    border-bottom: 1px solid {COLORS['border']};
}}

QListView::item:hover, QListWidget::item:hover {{
    background-color: {COLORS['surface']};
}}

QListView::item:selected, QListWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

/* Tree views */
QTreeView {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background-color: {COLORS['background']};
    alternate-background-color: {COLORS['surface']};
    selection-background-color: {COLORS['primary']};
    selection-color: white;
    outline: none;
}}

QTreeView::item {{
    padding: 4px;
    border-bottom: 1px solid {COLORS['border']};
}}

QTreeView::item:hover {{
    background-color: {COLORS['surface']};
}}

QTreeView::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

/* Scroll areas */
QScrollArea {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background-color: {COLORS['background']};
}}

/* Status bar */
QStatusBar {{
    background-color: {COLORS['surface']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
    font-size: 8pt;
}}

/* Menu bar */
QMenuBar {{
    background-color: {COLORS['background']};
    border-bottom: 1px solid {COLORS['border']};
    color: {COLORS['text']};
    font-size: 9pt;
}}

QMenuBar::item {{
    padding: 8px 12px;
    background-color: transparent;
}}

QMenuBar::item:hover {{
    background-color: {COLORS['surface']};
}}

QMenuBar::item:pressed {{
    background-color: {COLORS['primary']};
    color: white;
}}

/* Menus */
QMenu {{
    background-color: {COLORS['background']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 12px;
    border-radius: 4px;
}}

QMenu::item:hover {{
    background-color: {COLORS['primary']};
    color: white;
}}

/* Splitters */
QSplitter::handle {{
    background-color: {COLORS['border']};
    width: 3px;
    height: 3px;
}}

QSplitter::handle:hover {{
    background-color: {COLORS['primary']};
}}

/* Labels */
QLabel {{
    color: {COLORS['text']};
    font-size: 9pt;
}}

QLabel[class="title"] {{
    font-size: 14pt;
    font-weight: bold;
    color: {COLORS['text']};
    margin: 10px 0;
}}

QLabel[class="subtitle"] {{
    font-size: 11pt;
    font-weight: 500;
    color: {COLORS['text_secondary']};
    margin: 5px 0;
}}

QLabel[class="caption"] {{
    font-size: 8pt;
    color: {COLORS['text_secondary']};
}}

QLabel[class="success"] {{
    color: {COLORS['success']};
    font-weight: bold;
}}

QLabel[class="danger"] {{
    color: {COLORS['danger']};
    font-weight: bold;
}}

QLabel[class="warning"] {{
    color: {COLORS['warning']};
    font-weight: bold;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background-color: {COLORS['surface']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    min-height: 20px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_secondary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}

QScrollBar:horizontal {{
    background-color: {COLORS['surface']};
    height: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS['border']};
    min-width: 20px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['text_secondary']};
}}

/* Tab widget */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    background-color: {COLORS['background']};
}}

QTabBar::tab {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    padding: 8px 16px;
    margin-right: 2px;
    border-radius: 6px 6px 0 0;
    color: {COLORS['text_secondary']};
}}

QTabBar::tab:selected {{
    background-color: {COLORS['background']};
    border-bottom: 2px solid {COLORS['primary']};
    color: {COLORS['text']};
    font-weight: bold;
}}

QTabBar::tab:hover {{
    background-color: {COLORS['background']};
    color: {COLORS['text']};
}}
"""

def apply_button_style(button, style_class=""):
    """Apply style class to button"""
    if style_class:
        button.setProperty("class", style_class)
        button.style().polish(button)

def apply_label_style(label, style_class=""):
    """Apply style class to label"""
    if style_class:
        label.setProperty("class", style_class)
        label.style().polish(label)