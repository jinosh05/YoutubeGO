import os
import platform
import subprocess

def check_ffmpeg():
    try:
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

        if platform.system() == "Windows":
            result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True)
        else:
            result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)

        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip().splitlines()[0]
            if os.path.exists(ffmpeg_path) and os.access(ffmpeg_path, os.X_OK):
                test_cmd = f'"{ffmpeg_path}" -version'
                test_result = subprocess.run(test_cmd, shell=True, capture_output=True)
                if test_result.returncode == 0:
                    return True, ffmpeg_path

        common_paths = []
        if platform.system() == "Windows":
            common_paths = [
                os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "ffmpeg", "bin", "ffmpeg.exe"),
                os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "ffmpeg", "bin", "ffmpeg.exe")
            ]
        elif platform.system() == "Darwin":
            common_paths = [
                "/usr/local/bin/ffmpeg",
                "/opt/homebrew/bin/ffmpeg",
                os.path.expanduser("~/homebrew/bin/ffmpeg")
            ]
        else:
            common_paths = [
                "/usr/bin/ffmpeg",
                "/usr/local/bin/ffmpeg",
                "/snap/bin/ffmpeg"
            ]

        for path in common_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return True, path

        return False, ""

    except Exception as e:
        print(f"Error checking FFmpeg: {str(e)}")
        return False, "" 