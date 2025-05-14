from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        
        welcome_text = """Welcome to YoutubeGO 4.4.14

Usage Instructions:
- Home: Overview and instructions
- MP4: Download videos in MP4 format
- MP3: Download audio in MP3 format
- History: View your download history
- Settings: Configure resolution, proxy, download folder, etc.
- Profile: Update your user details
- Queue: Manage multiple downloads
- Scheduler: Schedule planned downloads

Visit youtubego.org for more details, check GitHub for source code."""

        lbl = QLabel(welcome_text)
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setOpenExternalLinks(True)
        layout.addWidget(lbl)
        
        layout.addStretch() 