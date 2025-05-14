import os
import platform
import subprocess
import sys

def check_ffmpeg():
    try:
       
        result = subprocess.run(
            ["where" if platform.system() == "Windows" else "which", "ffmpeg"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip().splitlines()[0]
            if os.path.exists(ffmpeg_path) and os.access(ffmpeg_path, os.X_OK):
                return True, ffmpeg_path
                
        return False, ""

    except Exception as e:
        print(f"[FFmpeg Detection Error] {e}")
        return False, ""
