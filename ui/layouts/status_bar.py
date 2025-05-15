from PySide6.QtWidgets import QStatusBar, QHBoxLayout, QLabel, QProgressBar, QWidget
from PySide6.QtCore import Qt
from ui.components.animated_button import AnimatedButton

class StatusBarLayout:
    def __init__(self, parent):
        self.parent = parent
        self.container = QStatusBar()
        self.progress_bar = None
        self.status_label = None
        self.ffmpeg_label = None
        self.show_logs_btn = None
        self.init_ui()

    def init_ui(self):
        layout_widget = QWidget()
        layout = QHBoxLayout(layout_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        self.show_logs_btn = AnimatedButton("Logs")
        self.show_logs_btn.setFixedWidth(60)
        self.show_logs_btn.clicked.connect(self.parent.log_manager.toggle_visibility)
        layout.addWidget(self.show_logs_btn)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label, stretch=1)

        self.ffmpeg_label = QLabel()
        self.ffmpeg_label.setMinimumWidth(120)
        self.ffmpeg_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.ffmpeg_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumWidth(200)
        self.progress_bar.setMaximumWidth(300)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.container.addPermanentWidget(layout_widget, 1)
        self.parent.setStatusBar(self.container) 