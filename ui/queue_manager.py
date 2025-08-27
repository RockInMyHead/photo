"""
Queue Manager for batch processing photos
"""

from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QProgressBar
from dataclasses import dataclass
from typing import List, Optional
import time
from enum import Enum


class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class ProcessingJob:
    job_id: str
    input_path: str
    output_path: str
    job_type: str  # "scan", "detect", "sort"
    status: JobStatus = JobStatus.PENDING
    progress: int = 0
    created_time: float = 0
    started_time: Optional[float] = None
    completed_time: Optional[float] = None
    error_message: Optional[str] = None
    files_total: int = 0
    files_processed: int = 0

    def __post_init__(self):
        if self.created_time == 0:
            self.created_time = time.time()


class QueueManager(QThread):
    """Manages processing queue for batch operations"""
    
    job_started = pyqtSignal(str)  # job_id
    job_progress = pyqtSignal(str, int, str)  # job_id, progress, message
    job_completed = pyqtSignal(str)  # job_id
    job_failed = pyqtSignal(str, str)  # job_id, error
    queue_status_changed = pyqtSignal(int, int)  # pending_count, completed_count

    def __init__(self):
        super().__init__()
        self.jobs: List[ProcessingJob] = []
        self.current_job: Optional[ProcessingJob] = None
        self.is_processing = False
        self.is_paused = False
        self.mutex = QMutex()
        
        # Processing components
        self.directory_scanner = None
        self.face_processor = None
        self.photo_sorter = None

    def add_job(self, job: ProcessingJob):
        """Add a job to the queue"""
        self.mutex.lock()
        try:
            self.jobs.append(job)
            self.queue_status_changed.emit(self.get_pending_count(), self.get_completed_count())
        finally:
            self.mutex.unlock()
        
        if not self.isRunning():
            self.start()

    def pause_queue(self):
        """Pause processing"""
        self.is_paused = True

    def resume_queue(self):
        """Resume processing"""
        self.is_paused = False

    def clear_completed(self):
        """Remove completed jobs from queue"""
        self.mutex.lock()
        try:
            self.jobs = [job for job in self.jobs if job.status not in [JobStatus.COMPLETED, JobStatus.FAILED]]
            self.queue_status_changed.emit(self.get_pending_count(), self.get_completed_count())
        finally:
            self.mutex.unlock()

    def get_pending_count(self) -> int:
        """Get number of pending jobs"""
        return len([job for job in self.jobs if job.status == JobStatus.PENDING])

    def get_completed_count(self) -> int:
        """Get number of completed jobs"""
        return len([job for job in self.jobs if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]])

    def get_jobs(self) -> List[ProcessingJob]:
        """Get copy of all jobs"""
        self.mutex.lock()
        try:
            return self.jobs.copy()
        finally:
            self.mutex.unlock()

    def run(self):
        """Main processing loop"""
        while True:
            if self.is_paused:
                self.msleep(1000)
                continue

            # Find next pending job
            next_job = None
            self.mutex.lock()
            try:
                for job in self.jobs:
                    if job.status == JobStatus.PENDING:
                        next_job = job
                        break
            finally:
                self.mutex.unlock()

            if next_job is None:
                # No pending jobs, wait
                self.msleep(1000)
                continue

            # Process the job
            self.process_job(next_job)

    def process_job(self, job: ProcessingJob):
        """Process a single job"""
        self.current_job = job
        job.status = JobStatus.PROCESSING
        job.started_time = time.time()
        
        self.job_started.emit(job.job_id)
        
        try:
            if job.job_type == "full_process":
                self.process_full_workflow(job)
            elif job.job_type == "scan":
                self.process_scan_job(job)
            elif job.job_type == "detect":
                self.process_detection_job(job)
            elif job.job_type == "sort":
                self.process_sorting_job(job)
            
            job.status = JobStatus.COMPLETED
            job.completed_time = time.time()
            self.job_completed.emit(job.job_id)
            
        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_time = time.time()
            self.job_failed.emit(job.job_id, str(e))
        
        finally:
            self.current_job = None
            self.queue_status_changed.emit(self.get_pending_count(), self.get_completed_count())

    def process_full_workflow(self, job: ProcessingJob):
        """Process complete workflow: scan -> detect -> sort"""
        # This would integrate with existing processors
        # For now, simulate the workflow
        
        stages = ["Сканирование файлов", "Обнаружение лиц", "Сортировка по группам", "Создание папок"]
        stage_progress = [0, 25, 50, 75, 100]
        
        for i, stage in enumerate(stages):
            if self.isInterruptionRequested():
                raise Exception("Операция отменена")
            
            self.job_progress.emit(job.job_id, stage_progress[i], stage)
            
            # Simulate processing time
            for progress in range(stage_progress[i], stage_progress[i + 1], 5):
                if self.isInterruptionRequested():
                    raise Exception("Операция отменена")
                
                self.job_progress.emit(job.job_id, progress, f"{stage}... {progress}%")
                self.msleep(100)  # Simulate work

    def process_scan_job(self, job: ProcessingJob):
        """Process scanning job"""
        self.job_progress.emit(job.job_id, 50, "Сканирование...")
        self.msleep(1000)  # Simulate
        
    def process_detection_job(self, job: ProcessingJob):
        """Process face detection job"""
        self.job_progress.emit(job.job_id, 50, "Обнаружение лиц...")
        self.msleep(2000)  # Simulate
        
    def process_sorting_job(self, job: ProcessingJob):
        """Process sorting job"""
        self.job_progress.emit(job.job_id, 50, "Сортировка...")
        self.msleep(1000)  # Simulate


class QueueWidget(QWidget):
    """Widget for displaying and managing the processing queue"""
    
    def __init__(self, queue_manager: QueueManager):
        super().__init__()
        self.queue_manager = queue_manager
        self.setup_ui()
        self.connect_signals()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_queue_display)
        self.update_timer.start(1000)  # Update every second

    def setup_ui(self):
        """Setup the queue widget UI"""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        self.queue_label = QLabel("Очередь обработки")
        self.queue_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(self.queue_label)
        
        # Queue controls
        self.pause_btn = QPushButton("⏸️ Пауза")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setMaximumWidth(100)
        header_layout.addWidget(self.pause_btn)
        
        self.clear_btn = QPushButton("🗑️ Очистить")
        self.clear_btn.clicked.connect(self.clear_completed)
        self.clear_btn.setMaximumWidth(100)
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # Status
        self.status_label = QLabel("Задач в очереди: 0 | Выполнено: 0")
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        # Queue list
        self.queue_list = QListWidget()
        self.queue_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
                alternate-background-color: #ecf0f1;
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
        layout.addWidget(self.queue_list)

    def connect_signals(self):
        """Connect queue manager signals"""
        self.queue_manager.job_started.connect(self.on_job_started)
        self.queue_manager.job_progress.connect(self.on_job_progress)
        self.queue_manager.job_completed.connect(self.on_job_completed)
        self.queue_manager.job_failed.connect(self.on_job_failed)
        self.queue_manager.queue_status_changed.connect(self.on_queue_status_changed)

    def toggle_pause(self):
        """Toggle pause/resume"""
        if self.queue_manager.is_paused:
            self.queue_manager.resume_queue()
            self.pause_btn.setText("⏸️ Пауза")
        else:
            self.queue_manager.pause_queue()
            self.pause_btn.setText("▶️ Продолжить")

    def clear_completed(self):
        """Clear completed jobs"""
        self.queue_manager.clear_completed()
        self.update_queue_display()

    def update_queue_display(self):
        """Update the queue display"""
        self.queue_list.clear()
        
        jobs = self.queue_manager.get_jobs()
        for job in jobs:
            status_icon = {
                JobStatus.PENDING: "⏳",
                JobStatus.PROCESSING: "⚙️",
                JobStatus.COMPLETED: "✅",
                JobStatus.FAILED: "❌",
                JobStatus.PAUSED: "⏸️"
            }.get(job.status, "❓")
            
            # Show folder name for full_process jobs
            if job.job_type == "full_process":
                folder_name = os.path.basename(job.input_path)
                item_text = f"{status_icon} 📂 {folder_name} - {job.progress}%"
            else:
                item_text = f"{status_icon} {job.job_type} - {job.progress}%"

            if job.status == JobStatus.PROCESSING and self.queue_manager.current_job == job:
                item_text += " (текущая)"
            elif job.status == JobStatus.FAILED:
                item_text += f" - {job.error_message}"
                
            self.queue_list.addItem(item_text)

    def on_job_started(self, job_id: str):
        """Handle job started"""
        self.update_queue_display()

    def on_job_progress(self, job_id: str, progress: int, message: str):
        """Handle job progress"""
        # Update the specific job's progress
        jobs = self.queue_manager.get_jobs()
        for job in jobs:
            if job.job_id == job_id:
                job.progress = progress
                break
        self.update_queue_display()

    def on_job_completed(self, job_id: str):
        """Handle job completed"""
        self.update_queue_display()

    def on_job_failed(self, job_id: str, error: str):
        """Handle job failed"""
        self.update_queue_display()

    def on_queue_status_changed(self, pending: int, completed: int):
        """Handle queue status change"""
        self.status_label.setText(f"Задач в очереди: {pending} | Выполнено: {completed}")
