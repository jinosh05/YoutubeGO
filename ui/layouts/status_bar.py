from PyQt5.QtWidgets import QStatusBar, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from ui.components.animated_button import AnimatedButton

class StatusBarLayout:
    def __init__(self, parent):
        self.parent = parent
        self.status_bar = QStatusBar(parent)
        self.init_ui()

    def init_ui(self):
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximumWidth(400)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("0%")
        self.progress_bar.setStyleSheet("font-weight: bold;")
        
        
        self.status_label = QLabel("Ready")
        
        
        if self.parent.ffmpeg_found:
            self.ffmpeg_label = QLabel("✓ FFmpeg Ready")
            self.ffmpeg_label.setStyleSheet("""
                color: #4CAF50;
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 10px;
                background: rgba(76, 175, 80, 0.1);
            """)
        else:
            self.ffmpeg_label = QLabel("⚠️ FFmpeg Required")
            self.ffmpeg_label.setStyleSheet("""
                color: #FFC107;
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 10px;
                background: rgba(255, 193, 7, 0.1);
            """)
        self.ffmpeg_label.setToolTip(self.parent.ffmpeg_path if self.parent.ffmpeg_found else "Please download FFmpeg from the official website")
        
        
        self.show_logs_btn = AnimatedButton("Logs")
        self.show_logs_btn.clicked.connect(self.parent.toggle_logs)
        
        
        self.status_bar.addWidget(self.show_logs_btn)
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.ffmpeg_label)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.parent.setStatusBar(self.status_bar) 