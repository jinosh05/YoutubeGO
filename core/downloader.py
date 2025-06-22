import os
import yt_dlp
import gc
import tempfile
from PySide6.QtCore import QRunnable, QObject, Signal
from core.utils import format_speed, format_time, get_data_dir
from core.history import add_history_entry
import time
import shutil
import json

class YTLogger:
    def __init__(self, log_signal):
        self.log_signal = log_signal
        self._temp_files = []

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

    def cleanup(self):
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self._temp_files.clear()

class DownloadTask:
    def __init__(self, url, resolution, folder, proxy, audio_only=False, playlist=False, subtitles=False, output_format="mp4", from_queue=False, audio_format=None):
        self.url = url
        self.resolution = resolution
        self.folder = folder
        self.proxy = proxy
        self.audio_only = audio_only
        self.playlist = playlist
        self.subtitles = subtitles
        self.output_format = output_format
        self.from_queue = from_queue
        self.audio_format = audio_format
        self._temp_dir = None

    def create_temp_dir(self):
        if not self._temp_dir:
            self._temp_dir = tempfile.mkdtemp()
        return self._temp_dir

    def cleanup(self):
        if self._temp_dir and os.path.exists(self._temp_dir):
            try:
                for file in os.listdir(self._temp_dir):
                    file_path = os.path.join(self._temp_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(self._temp_dir)
            except Exception:
                pass
            self._temp_dir = None

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
        self._ydl = None

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self._ydl:
            try:
                self._ydl.close()
            except Exception:
                pass
            self._ydl = None
        if self.logger:
            self.logger.cleanup()
        if self.task:
            self.task.cleanup()
        gc.collect()

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
        try:
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
                    self._ydl = ydl
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
                    
                    self.write_to_history(title, channel, self.task.url)

                download_options = self._get_base_options()
                temp_dir = self.task.create_temp_dir()
                download_options.update({
                    "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                    "progress_hooks": [self.progress_hook],
                    "noplaylist": not self.task.playlist,
                    "retries": 10,
                    "fragment_retries": 10,
                    "proxy": self.task.proxy if self.task.proxy else None,
                    "verbose": True,
                    "file_access_retries": 5,
                    "retry_sleep": 2,
                    "prefer_ffmpeg": True,
                })

                if hasattr(self.task, 'ffmpeg_path') and self.task.ffmpeg_path:
                    download_options["ffmpeg_location"] = self.task.ffmpeg_path
                    self.log_signal.emit(f"Using FFmpeg from: {self.task.ffmpeg_path}")

                if self.task.audio_only:
                    audio_format = self.task.audio_format if hasattr(self.task, 'audio_format') and self.task.audio_format else "mp3"
                    download_options.update({
                        "final_ext": audio_format,
                        "format": f"ba[acodec^={audio_format}]/ba/b",
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "nopostoverwrites": False,
                            "preferredcodec": audio_format,
                            "preferredquality": "0"
                        }]
                    })
                    self.log_signal.emit(f"Audio format set to: {audio_format}")
                else:
                    try:
                        download_options.update({
                            "format": self._get_format_string(),
                            "format_sort": ["res", "ext:mp4:m4a", "size", "br", "asr"],
                            "prefer_free_formats": False,
                            "merge_output_format": self.task.output_format.lower(),
                            "postprocessors": [{
                                "key": "FFmpegVideoRemuxer",
                                "preferedformat": self.task.output_format.lower(),
                                "when": "post_process"
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
                        self._ydl = ydl
                        try:
                            ydl.download([self.task.url])
                            self._move_files_to_final_location(temp_dir)
                        except Exception as e:
                            if "Unable to rename file" in str(e):
                                time.sleep(2)
                                ydl.download([self.task.url])
                                self._move_files_to_final_location(temp_dir)
                            elif "unable to obtain file audio codec" in str(e):
                                ydl_opts = download_options.copy()
                                ydl_opts['postprocessor_args'] = [
                                    '-ar', '44100',
                                    '-ac', '2',
                                    '-b:a', '192k',
                                    '-vn'
                                ]
                                with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                                    self._ydl = ydl2
                                    ydl2.download([self.task.url])
                                    self._move_files_to_final_location(temp_dir)
                            else:
                                raise
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
                                self._ydl = ydl
                                ydl.download([self.task.url])
                                self._move_files_to_final_location(temp_dir)
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
        finally:
            self.cleanup()

    def _move_files_to_final_location(self, temp_dir):
        if not os.path.exists(temp_dir):
            return
            
        for file in os.listdir(temp_dir):
            src_path = os.path.join(temp_dir, file)
            dst_path = os.path.join(self.task.folder, file)
            
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.move(src_path, dst_path)

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

    def write_to_history(self, title, channel, url):
       
        try:
            history_file = os.path.join(get_data_dir(), "history.json")
            
            # Load 
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            else:
                history = []
            
            # Add
            history.append({
                "title": title,
                "channel": channel,
                "url": url
            })
            
            # Save 
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
            self.log_signal.emit(f"Added to history: {title} - {channel}")
             
        except Exception as e:
            self.log_signal.emit(f"Error writing to history: {str(e)}")
