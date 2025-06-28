from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QGroupBox, QFormLayout, QLineEdit, QComboBox, 
                            QFileDialog, QMessageBox, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.components.animated_button import AnimatedButton
from core.version import get_version

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)
        
    
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        lbl = QLabel("Settings")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        
        version_label = QLabel(f"Version {get_version()}")
        version_label.setObjectName("version_label")
        version_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                padding: 6px 16px;
                border-radius: 15px;
                background: rgba(76, 175, 80, 0.1);
                font-size: 12pt;
                font-weight: bold;
                border: 1px solid rgba(76, 175, 80, 0.2);
                margin: 5px;
            }
            QLabel:hover {
                background: rgba(76, 175, 80, 0.15);
                border: 1px solid rgba(76, 175, 80, 0.3);
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setCursor(Qt.CursorShape.PointingHandCursor)
        version_label.mousePressEvent = lambda e: self.parent.check_for_updates()
        
        header_layout.addStretch()
        header_layout.addWidget(lbl, alignment=Qt.AlignCenter)
        header_layout.addStretch()
        header_layout.addWidget(version_label, alignment=Qt.AlignVCenter)
        
        layout.addWidget(header_container)

        # Concurrent Downloads Group
        g_con = QGroupBox("Max Concurrent Downloads")
        g_con.setMinimumWidth(300)
        g_layout = QHBoxLayout(g_con)
        g_layout.setContentsMargins(10, 10, 10, 10)
        self.concurrent_combo = QComboBox()
        self.concurrent_combo.addItems(["1","2","3","4","5","10"])
        self.concurrent_combo.setCurrentText(str(self.parent.max_concurrent_downloads))
        self.concurrent_combo.currentIndexChanged.connect(self.set_max_concurrent_downloads)
        g_layout.addWidget(QLabel("Concurrent:"))
        g_layout.addWidget(self.concurrent_combo)
        layout.addWidget(g_con)

        # Technical Group
        g_tech = QGroupBox("Technical / Appearance")
        g_tech.setMinimumWidth(300)
        fl = QFormLayout(g_tech)
        fl.setContentsMargins(10, 10, 10, 10)
        fl.setSpacing(10)
        self.proxy_edit = QLineEdit()
        self.proxy_edit.setText(self.parent.user_profile.get_proxy())
        self.proxy_edit.setPlaceholderText("Proxy or bandwidth limit...")
        self.proxy_edit.textChanged.connect(self.proxy_changed)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark","Light"])
        self.theme_combo.setCurrentText(self.parent.user_profile.get_theme())
        self.theme_combo.currentTextChanged.connect(self.theme_changed)
        fl.addRow("Proxy/BW:", self.proxy_edit)
        fl.addRow("Theme:", self.theme_combo)
        layout.addWidget(g_tech)

        # Resolution Group
        g_res = QGroupBox("Default Resolution")
        g_res.setMinimumWidth(300)
        r_hl = QHBoxLayout(g_res)
        r_hl.setContentsMargins(10, 10, 10, 10)
        self.res_combo = QComboBox()
        self.res_combo.addItems(["144p","240p","360p","480p","720p","1080p","1440p","2160p","4320p"])
        self.res_combo.setCurrentText(self.parent.user_profile.get_default_resolution())
        self.res_combo.currentTextChanged.connect(self.resolution_changed)
        r_hl.addWidget(QLabel("Resolution:"))
        r_hl.addWidget(self.res_combo)
        layout.addWidget(g_res)

        # Audio Format Group
        g_audio = QGroupBox("Audio Format")
        g_audio.setMinimumWidth(300)
        a_hl = QHBoxLayout(g_audio)
        a_hl.setContentsMargins(10, 10, 10, 10)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(self.parent.user_profile.get_available_audio_formats())
        self.audio_format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        self.audio_format_combo.currentTextChanged.connect(self.audio_format_changed)
        a_hl.addWidget(QLabel("Format:"))
        a_hl.addWidget(self.audio_format_combo)
        layout.addWidget(g_audio)

        # Download Path Group
        g_path = QGroupBox("Download Path")
        g_path.setMinimumWidth(300)
        p_hl = QHBoxLayout(g_path)
        p_hl.setContentsMargins(10, 10, 10, 10)
        self.download_path_edit = QLineEdit()
        self.download_path_edit.setReadOnly(True)
        self.download_path_edit.setText(self.parent.user_profile.get_download_path())
        b_br = AnimatedButton("Browse")
        b_br.clicked.connect(self.select_download_path)
        p_hl.addWidget(QLabel("Folder:"))
        p_hl.addWidget(self.download_path_edit)
        p_hl.addWidget(b_br)
        layout.addWidget(g_path)
        
        layout.addStretch()
        
        
        scroll.setWidget(container)

    def set_max_concurrent_downloads(self, idx):
        val = self.concurrent_combo.currentText()
        self.parent.max_concurrent_downloads = int(val)
        self.parent.append_log(f"Max concurrent downloads set to {val}")

    def proxy_changed(self, text):
        self.parent.user_profile.set_proxy(text)
        self.parent.append_log(f"Proxy setting updated: {text}")

    def theme_changed(self, theme):
        self.parent.user_profile.set_theme(theme)
        self.parent.theme_manager.change_theme(theme)
        self.parent.append_log(f"Theme changed to: {theme}")

    def resolution_changed(self, resolution):
        self.parent.user_profile.set_default_resolution(resolution)
        self.parent.append_log(f"Default resolution set to: {resolution}")

    def audio_format_changed(self, format):
        self.parent.user_profile.set_audio_format(format)
        self.parent.append_log(f"Audio format set to: {format}")

    def select_download_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.parent.user_profile.set_profile(
                self.parent.user_profile.data["name"],
                self.parent.user_profile.data["profile_picture"],
                folder
            )
            self.download_path_edit.setText(folder)
            self.parent.append_log(f"Download path changed to {folder}") 