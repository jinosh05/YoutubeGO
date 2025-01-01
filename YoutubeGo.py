
#                                                                             TOXİ360                                                                                                   # 

import sys
import os
import time
import threading
import yt_dlp

from PyQt5.QtCore import (
    Qt, pyqtSignal, QObject, QThreadPool, QRunnable
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, 
    QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, 
    QProgressBar, QDockWidget, QTextEdit, QStatusBar, QMenuBar, 
    QAction, QComboBox, QFileDialog, QMessageBox, QListWidget, 
    QListWidgetItem, QAbstractItemView, QTableWidget, QTableWidgetItem, 
    QHeaderView, QGroupBox, QFormLayout, QCheckBox, QDialog, 
    QDialogButtonBox
)

###############################################################################
#                               DARK THEME
###############################################################################
def apply_dark_theme(app):
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#2b2b2b"))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor("#3c3f41"))
    palette.setColor(QPalette.AlternateBase, QColor("#2b2b2b"))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor("#3c3f41"))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor("#444444"))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

###############################################################################
#                              DRAG & DROP
###############################################################################
class DragDropLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.acceptProposedAction()

    def dropEvent(self, e):
        txt = e.mimeData().text()
        if txt.startswith("http"):
            self.setText(txt)
        else:
            self.setText(txt.replace("file://", ""))

###############################################################################
#                              DOWNLOAD TASK
###############################################################################
class DownloadTask:
    def __init__(self, url, resolution, folder, audio_only, playlist, bandwidth):
        self.url = url
        self.resolution = resolution
        self.folder = folder
        self.audio_only = audio_only
        self.playlist = playlist
        self.bandwidth = bandwidth

###############################################################################
#                              QUEUE WORKER
###############################################################################
class DownloadQueueWorker(QRunnable):
    def __init__(self, task, progress_signal, status_signal):
        super().__init__()
        self.task = task
        self.progress_signal = progress_signal
        self.status_signal = status_signal
        self.pause = False
        self.cancel = False
        self.current_title = None
        self.partial_files = []

    def run(self):
       
        ydl_opts = {
            "outtmpl": f'{self.task.folder}/%(title)s.%(ext)s',
            "progress_hooks": [self.progress_hook],
            "noplaylist": not self.task.playlist
        }
        rate = self.convert_bandwidth(self.task.bandwidth)
        if rate is not None:
            ydl_opts["ratelimit"] = rate

        if self.task.audio_only:
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192"
                    }
                ]
            })
        else:
            if self.task.resolution == "4320":
                ydl_opts["format"] = "bestvideo[height<=4320]+bestaudio/best"
            elif self.task.resolution == "2160":
                ydl_opts["format"] = "bestvideo[height<=2160]+bestaudio/best"
            elif self.task.resolution == "1440":
                ydl_opts["format"] = "bestvideo[height<=1440]+bestaudio/best"
            elif self.task.resolution == "1080":
                ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best"
            else:
                ydl_opts["format"] = f'bestvideo[height<={self.task.resolution}]+bestaudio/best'
            ydl_opts["merge_output_format"] = "mp4"

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as y:
                y.download([self.task.url])
                self.status_signal.emit("Completed")
        except Exception as e:
            self.status_signal.emit(f"Error: {str(e)}")

    def progress_hook(self, d):
        if self.cancel:
            raise yt_dlp.utils.DownloadError("Cancelled")

        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes", 1)
            percent = (downloaded / total) * 100 if total > 0 else 0
            speed = d.get("speed", 0) or 0
            speed_mb = speed / 1024 / 1024
            filename = d.get("filename", "File").split("/")[-1]
            self.current_title = filename
            self.partial_files.append(d.get("filename"))
            self.progress_signal.emit(percent, speed_mb, filename)

        while self.pause:
            time.sleep(0.1)

    def pause_download(self):
        self.pause = True

    def resume_download(self):
        self.pause = False

    def cancel_download(self):
        self.cancel = True
        for f in set(self.partial_files):
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        self.status_signal.emit("Cancelled")

    def convert_bandwidth(self, b):
        if not b or b == "High Performance":
            return None
        elif b == "Balanced":
            return 5_000_000
        else:
            return 1_000_000

###############################################################################
#                              MAIN WINDOW
###############################################################################
class MainWindow(QMainWindow):
    progress_signal = pyqtSignal(float, float, str)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.worker = None
        self.bandwidth = "High Performance"
        self.download_history = []
        self.setWindowTitle("Universal Video Downloader")
        self.setGeometry(100, 100, 1280, 800)
        self.progress_signal.connect(self.update_progress)
        self.status_signal.connect(self.update_status)
        self.setup_ui()

    def setup_ui(self):
        self.setup_dark_theme()
        self.setup_menubar()
        self.setup_statusbar()
        self.create_dock_log()

        base_widget = QWidget()
        self.setCentralWidget(base_widget)
        main_layout = QHBoxLayout(base_widget)

        self.sidebar = QListWidget()
        self.sidebar.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sidebar.setFixedWidth(170)

        mp4_item = QListWidgetItem("MP4 Download")
        mp3_item = QListWidgetItem("MP3 Download")
        history_item = QListWidgetItem("History")
        settings_item = QListWidgetItem("Settings")
        queue_item = QListWidgetItem("Queue")

        self.sidebar.addItem(mp4_item)
        self.sidebar.addItem(mp3_item)
        self.sidebar.addItem(history_item)
        self.sidebar.addItem(settings_item)
        self.sidebar.addItem(queue_item)
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.sidebar_changed)

        main_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.page_mp4 = self.create_mp4_page()
        self.page_mp3 = self.create_mp3_page()
        self.page_history = self.create_history_page()
        self.page_settings = self.create_settings_page()
        self.page_queue = self.create_queue_page()

        self.stack.addWidget(self.page_mp4)
        self.stack.addWidget(self.page_mp3)
        self.stack.addWidget(self.page_history)
        self.stack.addWidget(self.page_settings)
        self.stack.addWidget(self.page_queue)

        self.stack.setCurrentIndex(0)

    def setup_dark_theme(self):
        apply_dark_theme(QApplication.instance())

    def setup_menubar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Quit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        insta_action = QAction("Instagram: fntxii", self)
        help_menu.addAction(insta_action)
        mail_action = QAction("E-Mail: toxi360@workmail.com", self)
        help_menu.addAction(mail_action)

    def setup_statusbar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        status_bar.addPermanentWidget(self.progress_bar)
        self.status_label = QLabel("Ready")
        status_bar.addWidget(self.status_label)

    def create_dock_log(self):
        self.log_dock = QDockWidget("Log", self)
        self.log_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(False)
        self.log_dock.setWidget(self.log_text_edit)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)

    def sidebar_changed(self, index):
        self.stack.setCurrentIndex(index)

    def create_mp4_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)

        form_box = QGroupBox("MP4 Download Settings")
        form_lay = QFormLayout(form_box)

        self.mp4_url = DragDropLineEdit()
        form_lay.addRow(QLabel("URL:"), self.mp4_url)

        h_folder = QHBoxLayout()
        self.mp4_folder = QLineEdit()
        b_browse = QPushButton("Browse")
        b_browse.clicked.connect(lambda: self.select_folder(self.mp4_folder))
        h_folder.addWidget(self.mp4_folder)
        h_folder.addWidget(b_browse)

        form_lay.addRow(QLabel("Folder:"), h_folder)
        lay.addWidget(form_box)

        btn_box = QHBoxLayout()
        b_single = QPushButton("Download Single MP4")
        b_single.clicked.connect(lambda: self.start_download_simple(self.mp4_url, self.mp4_folder, False, False))
        btn_box.addWidget(b_single)

        b_playlist = QPushButton("Download Playlist MP4")
        b_playlist.clicked.connect(lambda: self.start_download_simple(self.mp4_url, self.mp4_folder, False, True))
        btn_box.addWidget(b_playlist)

        lay.addLayout(btn_box)
        lay.addStretch()
        return w

    def create_mp3_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)

        form_box = QGroupBox("MP3 Download Settings")
        form_lay = QFormLayout(form_box)

        self.mp3_url = DragDropLineEdit()
        form_lay.addRow(QLabel("URL:"), self.mp3_url)

        h_folder = QHBoxLayout()
        self.mp3_folder = QLineEdit()
        b_browse = QPushButton("Browse")
        b_browse.clicked.connect(lambda: self.select_folder(self.mp3_folder))
        h_folder.addWidget(self.mp3_folder)
        h_folder.addWidget(b_browse)

        form_lay.addRow(QLabel("Folder:"), h_folder)
        lay.addWidget(form_box)

        btn_box = QHBoxLayout()
        b_single = QPushButton("Download Single MP3")
        b_single.clicked.connect(lambda: self.start_download_simple(self.mp3_url, self.mp3_folder, True, False))
        btn_box.addWidget(b_single)

        b_playlist = QPushButton("Download Playlist MP3")
        b_playlist.clicked.connect(lambda: self.start_download_simple(self.mp3_url, self.mp3_folder, True, True))
        btn_box.addWidget(b_playlist)

        lay.addLayout(btn_box)
        lay.addStretch()
        return w

    def create_history_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Title", "URL", "Type", "Status"])
        hh = self.history_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        lay.addWidget(self.history_table)

        srch_box = QHBoxLayout()
        self.search_box = QLineEdit()
        b_srch = QPushButton("Search")
        b_srch.clicked.connect(self.search_history)
        srch_box.addWidget(self.search_box)
        srch_box.addWidget(b_srch)
        lay.addLayout(srch_box)

        lay.addStretch()
        return w

    def create_settings_page(self):
        w = QWidget()
        main_lay = QVBoxLayout(w)

        group_res = QGroupBox("Resolution & Performance")
        form_lay = QFormLayout(group_res)

        self.res_combo = QComboBox()
        self.res_combo.addItems(["4320", "2160", "1440", "1080", "720", "480", "360", "240", "144"])
        form_lay.addRow(QLabel("Resolution:"), self.res_combo)

        self.bandwidth_combo = QComboBox()
        self.bandwidth_combo.addItems(["High Performance", "Balanced", "Normal"])
        self.bandwidth_combo.setCurrentText("High Performance")
        self.bandwidth_combo.currentTextChanged.connect(self.set_bandwidth)
        form_lay.addRow(QLabel("Performance:"), self.bandwidth_combo)

        main_lay.addWidget(group_res)
        group_res.setLayout(form_lay)

        ctrl_grp = QGroupBox("Controls")
        ctrl_lay = QHBoxLayout(ctrl_grp)

        b_pause = QPushButton("Pause")
        b_pause.clicked.connect(self.pause_active)
        ctrl_lay.addWidget(b_pause)

        b_resume = QPushButton("Resume")
        b_resume.clicked.connect(self.resume_active)
        ctrl_lay.addWidget(b_resume)

        b_cancel = QPushButton("Cancel")
        b_cancel.clicked.connect(self.cancel_active)
        ctrl_lay.addWidget(b_cancel)

        main_lay.addWidget(ctrl_grp)
        main_lay.addStretch()
        return w

    def create_queue_page(self):
        w = QWidget()
        lay = QVBoxLayout(w)

        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(5)
        self.queue_table.setHorizontalHeaderLabels(["URL", "Resolution", "Folder", "Type", "Status"])
        hh = self.queue_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        lay.addWidget(self.queue_table)

        btn_line = QHBoxLayout()
        b_add = QPushButton("Add to Queue")
        b_add.clicked.connect(self.add_queue_item_dialog)
        btn_line.addWidget(b_add)

        b_start = QPushButton("Start Queue")
        b_start.clicked.connect(self.start_queue)
        btn_line.addWidget(b_start)

        lay.addLayout(btn_line)
        lay.addStretch()
        return w

    def add_queue_item_dialog(self):
        d = QDialog(self)
        d.setWindowTitle("Add to Queue")
        ly = QVBoxLayout(d)
        form = QFormLayout()

        dd_url = DragDropLineEdit()
        dd_folder = QLineEdit()
        b_browse = QPushButton("Browse")

        def br():
            ff = QFileDialog.getExistingDirectory(self, "Select Folder")
            if ff:
                dd_folder.setText(ff)

        h = QHBoxLayout()
        h.addWidget(dd_folder)
        h.addWidget(b_browse)

        dd_res = QComboBox()
        dd_res.addItems(["4320", "2160", "1440", "1080", "720", "480", "360", "240", "144"])

        dd_perf = QComboBox()
        dd_perf.addItems(["High Performance", "Balanced", "Normal"])

        c_audio = QCheckBox()
        c_pl = QCheckBox()

        form.addRow("URL:", dd_url)
        form.addRow("Folder:", h)
        form.addRow("Resolution:", dd_res)
        form.addRow("Performance:", dd_perf)
        form.addRow("Audio Only:", c_audio)
        form.addRow("Playlist:", c_pl)

        ly.addLayout(form)

        b_ok = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        def on_ok():
            uu = dd_url.text().strip()
            ff = dd_folder.text().strip() or os.getcwd()
            rr = dd_res.currentText()
            pp = dd_perf.currentText()
            ao = c_audio.isChecked()
            pl = c_pl.isChecked()

            row = self.queue_table.rowCount()
            self.queue_table.insertRow(row)
            self.queue_table.setItem(row, 0, QTableWidgetItem(uu))
            self.queue_table.setItem(row, 1, QTableWidgetItem(rr))
            self.queue_table.setItem(row, 2, QTableWidgetItem(ff))
            dtp = "Audio" if ao else "Video"
            if pl:
                dtp += " Playlist"
            self.queue_table.setItem(row, 3, QTableWidgetItem(dtp))
            self.queue_table.setItem(row, 4, QTableWidgetItem("Waiting"))

            d.accept()

        def on_cancel():
            d.reject()

        b_ok.accepted.connect(on_ok)
        b_ok.rejected.connect(on_cancel)
        b_browse.clicked.connect(br)

        ly.addWidget(b_ok)
        d.exec_()

    def start_queue(self):
        for r in range(self.queue_table.rowCount()):
            st = self.queue_table.item(r, 4)
            if st and st.text() == "Waiting":
                url = self.queue_table.item(r, 0).text().strip()
                rr = self.queue_table.item(r, 1).text().strip()
                fld = self.queue_table.item(r, 2).text().strip()
                dtp = self.queue_table.item(r, 3).text().lower()
                audio = ("audio" in dtp)
                playlist = ("playlist" in dtp)
                task = DownloadTask(url, rr, fld, audio, playlist, self.bandwidth)
                self.run_task(task)
                self.queue_table.setItem(r, 4, QTableWidgetItem("Started"))
                break

    def set_bandwidth(self, val):
        self.bandwidth = val
        self.append_log(f"Performance set to {val}")

    def append_log(self, text):
        self.log_text_edit.append(text)

    def select_folder(self, edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            edit.setText(folder)

    def start_download_simple(self, url_edit, folder_edit, audio, playlist):
        u = url_edit.text().strip()
        f = folder_edit.text().strip() or os.getcwd()
        if not u:
            QMessageBox.warning(self, "Warning", "No URL specified.")
            return
        t = DownloadTask(u, self.res_combo.currentText(), f, audio, playlist, self.bandwidth)
        self.add_history_entry("(Pending)", u, ("Audio" if audio else "Video") + (" Playlist" if playlist else ""), "Starting")
        self.run_task(t)

    def run_task(self, task):
        w = DownloadQueueWorker(task, self.progress_signal, self.status_signal)
        self.worker = w
        self.threadpool.start(w)

    def update_progress(self, percent, speed, title):
        self.progress_bar.setValue(int(min(percent, 100)))
        self.status_label.setText(f"{title} - {percent:.2f}% @ {speed:.2f} MB/s")

    def update_status(self, st):
        self.status_label.setText(f"Status: {st}")
        self.append_log(f"Status: {st}")

    def add_history_entry(self, title, url, tp, stat):
        if not hasattr(self, "history_table"):
            return
        row = self.history_table.rowCount()
        self.history_table.insertRow(row)
        self.history_table.setItem(row, 0, QTableWidgetItem(title))
        self.history_table.setItem(row, 1, QTableWidgetItem(url))
        self.history_table.setItem(row, 2, QTableWidgetItem(tp))
        self.history_table.setItem(row, 3, QTableWidgetItem(stat))

    def pause_active(self):
        if self.worker:
            self.worker.pause_download()

    def resume_active(self):
        if self.worker:
            self.worker.resume_download()

    def cancel_active(self):
        if self.worker:
            self.worker.cancel_download()

    def search_history(self):
        txt = getattr(self, "search_box", QLineEdit()).text().strip().lower()
        if not hasattr(self, "history_table"):
            return
        for r in range(self.history_table.rowCount()):
            title = self.history_table.item(r, 0)
            url = self.history_table.item(r, 1)
            hide = True
            if title and url:
                if txt in title.text().lower() or txt in url.text().lower():
                    hide = False
            self.history_table.setRowHidden(r, hide)

###############################################################################
#                                   MAIN
###############################################################################
def main():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#                                                                                  TOXİ360                                                                                                    # 
