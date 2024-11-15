import sys
import os
import yt_dlp
import threading
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QProgressBar, QFileDialog, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class DownloadWorker(QObject):
    progress_signal = pyqtSignal(float, float, str)
    status_signal = pyqtSignal(str)
    
    def __init__(self, url, resolution, output_path, audio_only=False, is_playlist=False, bandwidth="1M"):
        super().__init__()
        self.url = url
        self.resolution = resolution
        self.output_path = output_path
        self.audio_only = audio_only
        self.is_playlist = is_playlist
        self.bandwidth = bandwidth if bandwidth is None else self.convert_bandwidth(bandwidth)
        self.pause = False
        self.cancel = False
        self.partial_files = []

    def convert_bandwidth(self, bandwidth):
        if bandwidth == "High Performance":
            return None  
        elif bandwidth == "Balanced":
            return 5000000  
        else:
            return 1000000  

    def run(self):
        if "youtube.com" not in self.url and "youtu.be" not in self.url:
            self.status_signal.emit("Error: Unsupported platform. Only YouTube links are allowed.")
            return

        ydl_opts = {
            'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
            'noplaylist': not self.is_playlist,
            'merge_output_format': 'mp4',
            'ratelimit': self.bandwidth
        }
        if self.audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        else:
            ydl_opts['format'] = f'bestvideo[height<={self.resolution}]+bestaudio/best'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                self.status_signal.emit("Completed")
        except Exception as e:
            self.status_signal.emit(f'Error: {str(e)}')

    def progress_hook(self, d):
        if self.cancel:
            raise yt_dlp.utils.DownloadError("Download cancelled")
        
        if d['status'] == 'downloading':
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes', 1)
            percent = float(downloaded_bytes) / float(total_bytes) * 100 if total_bytes > 0 else 0
            speed = d.get('speed', 0)
            speed = speed / 1024 / 1024 if speed is not None else 0  # MB/s
            title = d.get('filename', 'File').split('/')[-1]
            self.partial_files.append(d.get('filename'))
            self.progress_signal.emit(percent, speed, title)

        while self.pause:
            time.sleep(0.1) 

    def pause_download(self):
        self.pause = True

    def resume_download(self):
        self.pause = False

    def cancel_download(self):
        self.cancel = True
        
        for file in set(self.partial_files):  
            if file and os.path.exists(file):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")
        self.status_signal.emit("Cancelled")

class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YoutubeGOV2")
        self.setGeometry(200, 200, 800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QProgressBar {
                background-color: #3c3f41;
                border: 1px solid #555555;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3c3f41;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QLabel {
                font-size: 14px;
            }
        """)

    
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

       
        self.url_input = QLineEdit()
        self.layout.addWidget(QLabel("Download URL:"))
        self.layout.addWidget(self.url_input)

        self.output_folder = QLineEdit()
        self.layout.addWidget(QLabel("Save Folder:"))
        self.layout.addWidget(self.output_folder)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.browse_button)

        
        settings_layout = QHBoxLayout()
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(['1080', '720', '480', '360', '240', '144'])
        settings_layout.addWidget(QLabel("Resolution:"))
        settings_layout.addWidget(self.resolution_combo)

        self.bandwidth_combo = QComboBox()
        self.bandwidth_combo.addItems(["High Performance", "Balanced", "Normal"])
        self.bandwidth_combo.currentTextChanged.connect(self.set_bandwidth)
        settings_layout.addWidget(QLabel("Performance Mode:"))
        settings_layout.addWidget(self.bandwidth_combo)
        
        self.layout.addLayout(settings_layout)

        self.download_video_button = QPushButton("Download Video (MP4)")
        self.download_video_button.clicked.connect(lambda: self.start_download(audio_only=False, is_playlist=False))
        self.layout.addWidget(self.download_video_button)

        self.download_playlist_button = QPushButton("Download Playlist (MP4)")
        self.download_playlist_button.clicked.connect(lambda: self.start_download(audio_only=False, is_playlist=True))
        self.layout.addWidget(self.download_playlist_button)

        self.download_mp3_button = QPushButton("Download MP3")
        self.download_mp3_button.clicked.connect(lambda: self.start_download(audio_only=True, is_playlist=False))
        self.layout.addWidget(self.download_mp3_button)

        self.download_playlist_mp3_button = QPushButton("Download Playlist MP3")
        self.download_playlist_mp3_button.clicked.connect(lambda: self.start_download(audio_only=True, is_playlist=True))
        self.layout.addWidget(self.download_playlist_mp3_button)


        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_download)
        self.layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume")
        self.resume_button.clicked.connect(self.resume_download)
        self.layout.addWidget(self.resume_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.layout.addWidget(self.cancel_button)

        
        self.progress_bar = QProgressBar()
        self.layout.addWidget(QLabel("Download Progress:"))
        self.layout.addWidget(self.progress_bar)

        
        self.status_label = QLabel("Status: Waiting for input...")
        self.layout.addWidget(self.status_label)

       
        self.bandwidth = "1M"

    def set_bandwidth(self, value):
        self.bandwidth = value

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_folder.setText(folder)

    def start_download(self, audio_only=False, is_playlist=False):
        url = self.url_input.text()
        resolution = self.resolution_combo.currentText()
        output_path = self.output_folder.text() or os.getcwd()

        if not url or not output_path:
            QMessageBox.warning(self, "Missing Information", "Please enter both URL and save folder.")
            return

        self.worker = DownloadWorker(url, resolution, output_path, audio_only=audio_only, is_playlist=is_playlist, bandwidth=self.bandwidth)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.status_signal.connect(self.update_status)
        self.thread = threading.Thread(target=self.worker.run)
        self.thread.start()

    def update_progress(self, percent, speed, title):
        self.progress_bar.setValue(int(percent))
        self.status_label.setText(f"Downloading {title} - {percent:.2f}% at {speed:.2f} MB/s")

    def update_status(self, status):
        self.status_label.setText(f"Status: {status}")

    def pause_download(self):
        if not hasattr(self, 'worker'):
            QMessageBox.warning(self, "Error", "No download in progress to pause.")
            return
        self.worker.pause_download()
        self.status_label.setText("Status: Paused")

    def resume_download(self):
        if not hasattr(self, 'worker'):
            QMessageBox.warning(self, "Error", "No download in progress to resume.")
            return
        self.worker.resume_download()
        self.status_label.setText("Status: Resumed")

    def cancel_download(self):
        if not hasattr(self, 'worker'):
            QMessageBox.warning(self, "Error", "No download in progress to cancel.")
            return
        self.worker.cancel_download()
        self.status_label.setText("Status: Cancelled")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec_())
