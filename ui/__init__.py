"""
UI Package for Photo Sorting Application
"""

# Import only when explicitly requested to avoid circular imports
# and PyQt6 compatibility issues

__all__ = [
    'MainWindow',
    'PhotoViewer',
    'DirectoryScanner',
    'FaceProcessor',
    'MainWindowSimple',
    'SimpleFaceProcessor'
]

def _import_main_window():
    from .main_window import MainWindow
    return MainWindow

def _import_main_window_simple():
    from .main_window_simple import MainWindow
    return MainWindow

def _import_photo_viewer():
    from .photo_viewer import PhotoViewer
    return PhotoViewer

def _import_directory_scanner():
    from .directory_scanner import DirectoryScanner
    return DirectoryScanner

def _import_face_processor():
    from .face_processor import FaceProcessor
    return FaceProcessor

def _import_simple_face_processor():
    from .face_processor_simple import SimpleFaceProcessor
    return SimpleFaceProcessor
