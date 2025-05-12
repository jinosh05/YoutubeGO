from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QGroupBox, QFormLayout, QLineEdit, QComboBox, 
                            QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.components.animated_button import AnimatedButton

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 20)
        
        lbl = QLabel("Settings")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        
        version_label = QLabel("v4.4.12")
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

        
        g_con = QGroupBox("Max Concurrent Downloads")
        g_layout = QHBoxLayout(g_con)
        self.concurrent_combo = QComboBox()
        self.concurrent_combo.addItems(["1","2","3","4","5","10"])
        self.concurrent_combo.setCurrentText(str(self.parent.max_concurrent_downloads))
        self.concurrent_combo.currentIndexChanged.connect(self.set_max_concurrent_downloads)
        g_layout.addWidget(QLabel("Concurrent:"))
        g_layout.addWidget(self.concurrent_combo)
        layout.addWidget(g_con)

        
        g_tech = QGroupBox("Technical / Appearance")
        fl = QFormLayout(g_tech)
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

        
        g_res = QGroupBox("Default Resolution")
        r_hl = QHBoxLayout(g_res)
        self.res_combo = QComboBox()
        self.res_combo.addItems(["144p","240p","360p","480p","720p","1080p","1440p","2160p","4320p"])
        self.res_combo.setCurrentText(self.parent.user_profile.get_default_resolution())
        r_hl.addWidget(QLabel("Resolution:"))
        r_hl.addWidget(self.res_combo)
        a_btn = AnimatedButton("Apply")
        a_btn.clicked.connect(self.apply_resolution)
        r_hl.addWidget(a_btn)
        layout.addWidget(g_res)

        
        g_path = QGroupBox("Download Path")
        p_hl = QHBoxLayout(g_path)
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

    def set_max_concurrent_downloads(self, idx):
        val = self.concurrent_combo.currentText()
        self.parent.max_concurrent_downloads = int(val)
        self.parent.append_log(f"Max concurrent downloads set to {val}")

    def change_theme_clicked(self):
        theme = self.theme_combo.currentText()
        self.parent.user_profile.set_theme(theme)
        if theme == "Dark":
            self.parent.setStyleSheet(self.parent.get_dark_theme())
        else:
            self.parent.setStyleSheet(self.parent.get_light_theme())
        self.parent.append_log(f"Theme changed to '{theme}'.")

    def apply_resolution(self):
        sr = self.res_combo.currentText()
        self.parent.user_profile.set_default_resolution(sr)
        prx = self.proxy_edit.text().strip()
        self.parent.user_profile.set_proxy(prx)
        self.parent.append_log(f"Resolution set: {sr}, Proxy: {prx}")
        QMessageBox.information(self, "Settings", f"Resolution: {sr}\nProxy: {prx}")

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