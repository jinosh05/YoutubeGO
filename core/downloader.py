import os
import yt_dlp
import shutil
import subprocess
import time
import platform
from PyQt5.QtCore import QRunnable
from core.utils import format_speed, format_time

class DownloadTask:
    def __init__(self, url, resolution, folder, proxy, audio_only=False, playlist=False, subtitles=False, output_format="mp4", from_queue=False):
        self.url = url
        self.resolution = resolution
        self.folder = folder
        self.proxy = proxy
        self.audio_only = audio_only
        self.playlist = playlist
        self.subtitles = subtitles
        self.output_format = output_format
        self.from_queue = from_queue

class DownloadQueueWorker(QRunnable):
    def __init__(self, task, row, progress_signal, status_signal, log_signal, info_signal=None):
        super().__init__()
        self.task = task
        self.row = row
        self.progress_signal = progress_signal
        self.status_signal = status_signal
        self.log_signal = log_signal
        self.info_signal = info_signal
        self.cancel = False

    def run(self):
        
        if not os.path.exists("youtube_cookies.txt"):
            try:
                with open("youtube_cookies.txt", "w") as cf:
                    cf.write("# Netscape HTTP Cookie File\nyoutube.com\tFALSE\t/\tFALSE\t0\tCONSENT\tYES+42\n")
            except Exception as e:
                self.log_signal.emit(f"Cookie file oluşturulamadı: {str(e)}")
        
        ydl_opts_info = {
            "quiet": True,
            "skip_download": True,
            "cookiefile": "youtube_cookies.txt",
            "ignoreerrors": True
        }

        if self.task.playlist:
            self.log_signal.emit("Playlist indexing in progress...")

      
        try:
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(self.task.url, download=False)
                if info is None:
                    self.status_signal.emit(self.row, "Video Unavailable")
                    self.log_signal.emit(f"Failed to extract info from: {self.task.url}\nThe video may be private, deleted, or age-restricted.")
                    return

                
                if "entries" in info and isinstance(info["entries"], list):
                    if info["entries"] and info["entries"][0]:
                        info = info["entries"][0]
                    else:
                        self.status_signal.emit(self.row, "Playlist Error")
                        self.log_signal.emit(f"Playlist entries not found or empty for: {self.task.url}")
                        return

                if "formats" in info:
                    self.log_signal.emit("\nAvailable formats:")
                    for f in info["formats"]:
                        if f.get("vcodec") != "none" and f.get("acodec") != "none":
                            self.log_signal.emit(f"Format: {f.get('format_id')} | Resolution: {f.get('width')}x{f.get('height')} | Ext: {f.get('ext')}")

                title = info.get("title", "No Title")
                channel = info.get("uploader", "Unknown Channel")
                if self.info_signal is not None and self.row is not None:
                    self.info_signal.emit(self.row, title, channel)
        except Exception as e:
            self.status_signal.emit(self.row, "Download Error")
            self.log_signal.emit(f"Failed to fetch video info for {self.task.url}\n{str(e)}")
            return

        
        ydl_opts_download = {
            "outtmpl": os.path.join(self.task.folder, "%(title)s.%(ext)s"),
            "progress_hooks": [self.progress_hook],
            "noplaylist": not self.task.playlist,
            "cookiefile": "youtube_cookies.txt",
            "retries": 10,
            "fragment_retries": 10,
            "retry_sleep_functions": lambda retries: 5,
            "ignoreerrors": True,
            "proxy": self.task.proxy if self.task.proxy else None,
            "socket_timeout": 10
        }

        if self.task.audio_only:
            ydl_opts_download["final_ext"] = "mp3"
            ydl_opts_download["format"] = "ba/b"
            ydl_opts_download["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "nopostoverwrites": False,
                "preferredcodec": "mp3",
                "preferredquality": "0"
            }]
        else:
            if self.task.resolution == "144p":
                format_str = "(bestvideo[height=144]/bestvideo[height<=144]/best[height<=144])+bestaudio/best"
            elif self.task.resolution == "240p":
                format_str = "(bestvideo[height=240]/bestvideo[height<=240]/best[height<=240])+bestaudio/best"
            elif self.task.resolution == "360p":
                format_str = "(bestvideo[height=360]/bestvideo[height<=360]/best[height<=360])+bestaudio/best"
            elif self.task.resolution == "480p":
                format_str = "(bestvideo[height=480]/bestvideo[height<=480]/best[height<=480])+bestaudio/best"
            elif self.task.resolution == "720p":
                format_str = "(bestvideo[height=720]/bestvideo[height<=720]/best[height<=720])+bestaudio/best"
            elif self.task.resolution == "1080p":
                format_str = "(bestvideo[height=1080]/bestvideo[height<=1080]/best[height<=1080])+bestaudio/best"
            elif self.task.resolution == "1440p":
                format_str = "(bestvideo[height=1440]/bestvideo[height<=1440]/best[height<=1440])+bestaudio/best"
            elif self.task.resolution == "2160p":
                format_str = "(bestvideo[height=2160]/bestvideo[height<=2160]/best[height<=2160])+bestaudio/best"
            elif self.task.resolution == "4320p":
                format_str = "(bestvideo[height=4320]/bestvideo[height<=4320]/best[height<=4320])+bestaudio/best"
            else:
                format_str = "bestvideo+bestaudio/best"

            if self.task.audio_only:
                format_str = "bestaudio/best"

            ydl_opts_download["format"] = format_str
            ydl_opts_download["format_sort"] = ["res", "ext:mp4:m4a", "size", "br", "asr"]
            ydl_opts_download["prefer_free_formats"] = False
            ydl_opts_download["retries"] = 10
            ydl_opts_download["fragment_retries"] = 10
            ydl_opts_download["retry_sleep_functions"] = lambda retries: 5
            ydl_opts_download["format_selector"] = "best"
            
            if self.task.output_format.lower() == "mp4":
                ydl_opts_download["merge_output_format"] = "mp4"
            else:
                ydl_opts_download["merge_output_format"] = self.task.output_format

            ydl_opts_download["postprocessors"] = [{
                "key": "FFmpegVideoRemuxer",
                "preferedformat": self.task.output_format.lower()
            }]

        if self.task.subtitles:
            ydl_opts_download["writesubtitles"] = True
            ydl_opts_download["allsubtitles"] = True

       
        try:
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([self.task.url])
            self.status_signal.emit(self.row, "Download Completed")
        except yt_dlp.utils.DownloadError as e:
            if self.cancel:
                self.status_signal.emit(self.row, "Download Cancelled")
                self.log_signal.emit("Download Cancelled")
            else:
                self.status_signal.emit(self.row, "Download Error")
                self.log_signal.emit(f"Download Error:\n{str(e)}")
        except Exception as e:
            self.status_signal.emit(self.row, "Download Error")
            self.log_signal.emit(f"Unexpected Error:\n{str(e)}")

    def progress_hook(self, d):
        if self.cancel:
            raise yt_dlp.utils.DownloadError("Cancelled")
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0) or 0
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            percent = (downloaded / total) * 100 if total > 0 else 0
            speed = d.get("speed", 0) or 0
            eta = d.get("eta", 0) or 0
            self.progress_signal.emit(self.row, percent)
            self.log_signal.emit(f"Downloading... {int(percent)}% | Speed: {format_speed(speed)} | ETA: {format_time(eta)}")
