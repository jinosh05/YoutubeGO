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
        
        version_label = QLabel(get_version())
        version_label.setStyleSheet("""
            QLabel {
                color: #ff4444;
                padding: 4px 12px;
                border-radius: 10px;
                background: rgba(255, 68, 68, 0.1);
                font-size: 11pt;
                font-weight: bold;
            }
        """)
        
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
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark","Light"])
        self.theme_combo.setCurrentText(self.parent.user_profile.get_theme())
        fl.addRow("Proxy/BW:", self.proxy_edit)
        fl.addRow("Theme:", self.theme_combo)
        theme_btn = AnimatedButton("Apply Theme")
        theme_btn.clicked.connect(self.change_theme_clicked)
        fl.addWidget(theme_btn)
        layout.addWidget(g_tech)

        # Resolution Group
        g_res = QGroupBox("Default Resolution")
        g_res.setMinimumWidth(300)
        r_hl = QHBoxLayout(g_res)
        r_hl.setContentsMargins(10, 10, 10, 10)
        self.res_combo = QComboBox()
        self.res_combo.addItems(["144p","240p","360p","480p","720p","1080p","1440p","2160p","4320p"])
        self.res_combo.setCurrentText(self.parent.user_profile.get_default_resolution())
        r_hl.addWidget(QLabel("Resolution:"))
        r_hl.addWidget(self.res_combo)
        a_btn = AnimatedButton("Apply")
        a_btn.clicked.connect(self.apply_resolution)
        r_hl.addWidget(a_btn)
        layout.addWidget(g_res)

        # Audio Format Group
        g_audio = QGroupBox("Audio Format")
        g_audio.setMinimumWidth(300)
        a_hl = QHBoxLayout(g_audio)
        a_hl.setContentsMargins(10, 10, 10, 10)
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(self.parent.user_profile.get_available_audio_formats())
        self.audio_format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        a_hl.addWidget(QLabel("Format:"))
        a_hl.addWidget(self.audio_format_combo)
        audio_btn = AnimatedButton("Apply")
        audio_btn.clicked.connect(self.apply_audio_format)
        a_hl.addWidget(audio_btn)
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
        
        # Scroll area'ya container'ı ekle
        scroll.setWidget(container)

    def set_max_concurrent_downloads(self, idx):
        val = self.concurrent_combo.currentText()
        self.parent.max_concurrent_downloads = int(val)
        self.parent.append_log(f"Max concurrent downloads set to {val}")

    def change_theme_clicked(self):
        theme = self.theme_combo.currentText()
        self.parent.theme_manager.change_theme(theme)

    def apply_resolution(self):
        sr = self.res_combo.currentText()
        self.parent.user_profile.set_default_resolution(sr)
        prx = self.proxy_edit.text().strip()
        self.parent.user_profile.set_proxy(prx)
        self.parent.append_log(f"Resolution set: {sr}, Proxy: {prx}")
        QMessageBox.information(self, "Settings", f"Resolution: {sr}\nProxy: {prx}")

    def apply_audio_format(self):
        audio_format = self.audio_format_combo.currentText()
        self.parent.user_profile.set_audio_format(audio_format)
        self.parent.append_log(f"Audio format set to: {audio_format}")
        QMessageBox.information(self, "Settings", f"Audio format set to: {audio_format}")

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