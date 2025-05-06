import os
import yt_dlp
from PyQt5.QtCore import QRunnable
from core.utils import format_speed, format_time, get_data_dir

class YTLogger:
    def __init__(self, log_signal):
        self.log_signal = log_signal

    def _log(self, level, msg):
        if msg.strip():
            self.log_signal.emit(f"[yt-dlp {level}] {msg}")

    def debug(self, msg):
        self._log("Debug", msg)

    def info(self, msg):
        self._log("Info", msg)

    def warning(self, msg):
        self._log("Warning", msg)

    def error(self, msg):
        self._log("Error", msg)

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
        self.data_dir = get_data_dir()
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.cookie_file = os.path.join(self.data_dir, "youtube_cookies.txt")
        self.logger = YTLogger(log_signal)

    def _get_base_options(self):
        return {
            "cookiefile": self.cookie_file,
            "ignoreerrors": True,
            "quiet": False,
            "no_warnings": False,
            "logger": self.logger,
            "socket_timeout": 10,
            "updatetime": False,
            "geo_bypass": True,
            "geo_bypass_country": "US",
            "force_ipv4": True
        }

    def _get_format_string(self):
        resolutions = {
            "144p": 144, "240p": 240, "360p": 360,
            "480p": 480, "720p": 720, "1080p": 1080,
            "1440p": 1440, "2160p": 2160, "4320p": 4320
        }
        if self.task.resolution in resolutions:
            height = resolutions[self.task.resolution]
            return f"(bestvideo[height<={height}]+bestaudio/best[height<={height}]/best)"
        return "bestvideo+bestaudio/best"

    def run(self):
        if not os.path.exists(self.cookie_file):
            try:
                with open(self.cookie_file, "w") as cf:
                    cf.write("# Netscape HTTP Cookie File\nyoutube.com\tFALSE\t/\tFALSE\t0\tCONSENT\tYES+42\n")
            except Exception as e:
                self.log_signal.emit(f"Failed to create cookie file: {str(e)}")

        info_options = self._get_base_options()
        info_options.update({
            "skip_download": True
        })

        if self.task.playlist:
            self.log_signal.emit("Playlist indexing in progress...")

        try:
            with yt_dlp.YoutubeDL(info_options) as ydl:
                info = ydl.extract_info(self.task.url, download=False)
                if info is None:
                    self.status_signal.emit(self.row, "Content Unavailable")
                    error_msg = f"Failed to extract info from: {self.task.url}\n"
                    error_msg += "Error Details:\n"
                    error_msg += "- HTTP Status: Content not found (404)\n"
                    error_msg += "Possible reasons:\n"
                    error_msg += "- Content might be private or deleted\n"
                    error_msg += "- Age restrictions may apply\n"
                    error_msg += "- Service restrictions (e.g., DRM protection)\n"
                    error_msg += "- Invalid or expired link\n"
                    error_msg += "- Platform limitations or regional restrictions"
                    self.log_signal.emit(error_msg)
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

            download_options = self._get_base_options()
            download_options.update({
                "outtmpl": os.path.join(self.task.folder, "%(title)s.%(ext)s"),
                "progress_hooks": [self.progress_hook],
                "noplaylist": not self.task.playlist,
                "retries": 10,
                "fragment_retries": 10,
                "proxy": self.task.proxy if self.task.proxy else None,
                "verbose": True
            })

            if self.task.audio_only:
                download_options.update({
                    "final_ext": "mp3",
                    "format": "ba[acodec^=mp3]/ba/b",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "nopostoverwrites": False,
                        "preferredcodec": "mp3",
                        "preferredquality": "0"
                    }]
                })
            else:
                try:
                    download_options.update({
                        "format": self._get_format_string(),
                        "format_sort": ["res", "ext:mp4:m4a", "size", "br", "asr"],
                        "prefer_free_formats": False,
                        "merge_output_format": self.task.output_format.lower(),
                        "postprocessors": [{
                            "key": "FFmpegVideoRemuxer",
                            "preferedformat": self.task.output_format.lower()
                        }]
                    })
                except Exception as e:
                    self.log_signal.emit(f"Format configuration failed, falling back to basic format: {str(e)}")
                    download_options["format"] = "best"

            if self.task.subtitles:
                download_options.update({
                    "writesubtitles": True,
                    "allsubtitles": True
                })

            try:
                with yt_dlp.YoutubeDL(download_options) as ydl:
                    ydl.download([self.task.url])
                self.status_signal.emit(self.row, "Download Completed")
            except yt_dlp.utils.DownloadError as e:
                if self.cancel:
                    self.status_signal.emit(self.row, "Download Cancelled")
                    self.log_signal.emit("Download Cancelled")
                else:
                    error_msg = f"Download Error: {str(e)}\n"
                    if hasattr(e, 'exc_info') and e.exc_info[1]:
                        error_msg += f"Error Type: {type(e.exc_info[1]).__name__}\n"
                        if hasattr(e.exc_info[1], 'code'):
                            error_msg += f"HTTP Status Code: {e.exc_info[1].code}\n"
                    self.log_signal.emit(error_msg)
                    self.log_signal.emit(f"Attempting download with basic format...")
                    download_options["format"] = "best"
                    try:
                        with yt_dlp.YoutubeDL(download_options) as ydl:
                            ydl.download([self.task.url])
                        self.status_signal.emit(self.row, "Download Completed (Basic Format)")
                    except Exception as e2:
                        self.status_signal.emit(self.row, "Download Error")
                        error_msg = f"All download attempts failed:\n"
                        error_msg += f"Error Type: {type(e2).__name__}\n"
                        error_msg += f"Error Details: {str(e2)}\n"
                        if hasattr(e2, 'code'):
                            error_msg += f"HTTP Status Code: {e2.code}\n"
                        self.log_signal.emit(error_msg)
        except Exception as e:
            self.status_signal.emit(self.row, "Download Error")
            error_msg = f"Unexpected Error:\n"
            error_msg += f"Error Type: {type(e).__name__}\n"
            error_msg += f"Error Details: {str(e)}\n"
            if hasattr(e, 'code'):
                error_msg += f"HTTP Status Code: {e.code}\n"
            self.log_signal.emit(error_msg)

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
