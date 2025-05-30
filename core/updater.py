import os
import sys
import json
import platform
import requests
import subprocess
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QThread, Qt
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QLabel
from core.version import VERSION, get_version

class UpdateChecker(QObject):
    update_available = Signal(str, str)
    update_error = Signal(str)
    download_progress = Signal(int)
    download_complete = Signal(str)
    version_status = Signal(str, str)  

    def __init__(self):
        super().__init__()
        self.current_version = VERSION
        self.github_api_url = "https://api.github.com/repos/Efeckc17/YouTubeGO/releases/latest"
        self.is_windows = platform.system() == "Windows"
        self.is_linux = platform.system() == "Linux"
        self.headers = {
            "User-Agent": f"YouTubeGO/{VERSION} ({platform.system()} {platform.release()})",
            "Accept": "application/vnd.github.v3+json"
        }

    def check_for_updates(self):
        try:
            response = requests.get(self.github_api_url, headers=self.headers)
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data["tag_name"]
                
                if self._compare_versions(latest_version, self.current_version) > 0:
                    download_url = None
                    for asset in release_data["assets"]:
                        if self.is_windows and asset["name"] == "YoutubeGo.exe":
                            download_url = asset["browser_download_url"]
                            break
                        elif self.is_linux and asset["name"] == "YoutubeGo-x86_64.AppImage":
                            download_url = asset["browser_download_url"]
                            break
                    
                    if download_url:
                        self.update_available.emit(latest_version, download_url)
                        self.version_status.emit(f"Update to {latest_version} available", "update-available")
                    else:
                        self.update_error.emit("No suitable update file found for your system")
                        self.version_status.emit("No update file found", "error")
                else:
                    self.version_status.emit("Up to date", "up-to-date")
            else:
                self.update_error.emit(f"Failed to check for updates: {response.status_code}")
                self.version_status.emit("Update check failed", "error")
        except Exception as e:
            self.update_error.emit(f"Error checking for updates: {str(e)}")
            self.version_status.emit("Update check failed", "error")

    def _compare_versions(self, version1, version2):
        v1_parts = [int(x) for x in version1.lstrip('v').split('.')]
        v2_parts = [int(x) for x in version2.lstrip('v').split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1 = v1_parts[i] if i < len(v1_parts) else 0
            v2 = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0

class UpdateDownloader(QThread):
    progress = Signal(int)
    complete = Signal(str)
    error = Signal(str)

    def __init__(self, url, target_path):
        super().__init__()
        self.url = url
        self.target_path = target_path
        self.headers = {
            "User-Agent": f"YouTubeGO/{VERSION} ({platform.system()} {platform.release()})",
            "Accept": "application/octet-stream"
        }

    def run(self):
        try:
            response = requests.get(self.url, stream=True, headers=self.headers)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0

            with open(self.target_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    file.write(data)
                    if total_size > 0:
                        progress = int((downloaded / total_size) * 100)
                        self.progress.emit(progress)

            self.complete.emit(self.target_path)
        except Exception as e:
            self.error.emit(str(e))

class UpdateManager:
    def __init__(self, parent=None):
        self.parent = parent
        self.checker = UpdateChecker()
        self.checker.update_available.connect(self._handle_update_available)
        self.checker.update_error.connect(self._handle_update_error)
        self.checker.version_status.connect(self._handle_version_status)
        self.downloader = None
        self.progress_dialog = None

    def check_for_updates(self):
        self.checker.check_for_updates()

    def _handle_update_available(self, version, download_url):
        reply = QMessageBox.question(
            self.parent,
            "Update Available",
            f"A new version ({version}) is available. Would you like to update now?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self._start_download(download_url)

    def _handle_update_error(self, error_message):
        QMessageBox.warning(self.parent, "Update Error", error_message)

    def _handle_version_status(self, status, status_type):
        if hasattr(self.parent, 'page_settings'):
            version_label = self.parent.page_settings.findChild(QLabel, "version_label")
            if version_label:
                version_label.setText(f"Version {get_version()} • {status}")
                if status_type == "up-to-date":
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
                elif status_type == "update-available":
                    version_label.setStyleSheet("""
                        QLabel {
                            color: #FFC107;
                            padding: 6px 16px;
                            border-radius: 15px;
                            background: rgba(255, 193, 7, 0.1);
                            font-size: 12pt;
                            font-weight: bold;
                            border: 1px solid rgba(255, 193, 7, 0.2);
                            margin: 5px;
                        }
                        QLabel:hover {
                            background: rgba(255, 193, 7, 0.15);
                            border: 1px solid rgba(255, 193, 7, 0.3);
                        }
                    """)
                else:  # error
                    version_label.setStyleSheet("""
                        QLabel {
                            color: #F44336;
                            padding: 6px 16px;
                            border-radius: 15px;
                            background: rgba(244, 67, 54, 0.1);
                            font-size: 12pt;
                            font-weight: bold;
                            border: 1px solid rgba(244, 67, 54, 0.2);
                            margin: 5px;
                        }
                        QLabel:hover {
                            background: rgba(244, 67, 54, 0.15);
                            border: 1px solid rgba(244, 67, 54, 0.3);
                        }
                    """)

    def _start_download(self, download_url):
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_path = os.path.join(app_dir, "YoutubeGo.exe" if platform.system() == "Windows" else "YoutubeGo-x86_64.AppImage")

        self.progress_dialog = QProgressDialog("Downloading update...", "Cancel", 0, 100, self.parent)
        self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setAutoReset(True)

        self.downloader = UpdateDownloader(download_url, target_path)
        self.downloader.progress.connect(self.progress_dialog.setValue)
        self.downloader.complete.connect(self._handle_download_complete)
        self.downloader.error.connect(self._handle_download_error)
        self.downloader.start()

    def _handle_download_complete(self, file_path):
        self.progress_dialog.close()
        reply = QMessageBox.question(
            self.parent,
            "Update Downloaded",
            "Update has been downloaded. Would you like to install it now?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self._install_update(file_path)

    def _handle_download_error(self, error_message):
        self.progress_dialog.close()
        QMessageBox.critical(self.parent, "Download Error", f"Failed to download update: {error_message}")

    def _install_update(self, file_path):
        try:
            if platform.system() == "Windows":
                subprocess.Popen([file_path, "--update"])
            else:
                os.chmod(file_path, 0o755)
                subprocess.Popen([file_path, "--update"])
            sys.exit(0)
        except Exception as e:
            QMessageBox.critical(self.parent, "Installation Error", f"Failed to install update: {str(e)}") 