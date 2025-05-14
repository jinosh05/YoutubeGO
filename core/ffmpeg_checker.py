import os
import platform
import subprocess
import sys

def check_ffmpeg():
    try:
        if getattr(sys, 'frozen', False):  
            app_dir = os.path.dirname(sys.executable)
        elif "APPDIR" in os.environ:       
            app_dir = os.environ["APPDIR"]
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))

        candidates = []

        if platform.system() == "Windows":
            candidates += [
                os.path.join(app_dir, "ffmpeg.exe"),
                os.path.join(app_dir, "bin", "ffmpeg.exe"),
                os.path.join(app_dir, "resources", "ffmpeg.exe"),
            ]
        else:
            candidates += [
                os.path.join(app_dir, "ffmpeg"),
                os.path.join(app_dir, "bin", "ffmpeg"),
                os.path.join(app_dir, "resources", "ffmpeg"),
                os.path.join(app_dir, "usr", "share", "youtubego", "resources", "ffmpeg"),
                os.path.join(os.path.dirname(app_dir), "Resources", "ffmpeg"),
            ]

        for path in candidates:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return True, path

        result = subprocess.run(
            ["where" if platform.system() == "Windows" else "which", "ffmpeg"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip().splitlines()[0]
            if os.path.exists(ffmpeg_path) and os.access(ffmpeg_path, os.X_OK):
                test_result = subprocess.run([ffmpeg_path, "-version"], capture_output=True)
                if test_result.returncode == 0:
                    return True, ffmpeg_path

        return False, ""

    except Exception as e:
        print(f"[FFmpeg Detection Error] {e}")
        return False, ""
