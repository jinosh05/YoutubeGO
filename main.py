import sys
import os
import atexit
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory, QSystemSemaphore, Qt
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from core.ffmpeg_checker import check_ffmpeg
from core.version import get_version

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def set_windows_app_id():
    if sys.platform.startswith("win"):
        try:
            app_id = f"YoutubeGO.App.{get_version(short=True)}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            
            # Set process DPI awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
            
            # Set up Windows taskbar icon
            myappid = f'YoutubeGO.{get_version()}'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Failed to set Windows app ID: {e}")
            pass

def cleanup_shared_memory(shared_mem):
    if shared_mem.isAttached():
        shared_mem.detach()
    if shared_mem.isAttached():
        shared_mem.forceDetach()

def main():
    set_windows_app_id()
    
    shared_mem = QSharedMemory(f"YoutubeGO {get_version(short=True)}")
    semaphore = QSystemSemaphore(f"YoutubeGO_Semaphore_{get_version(short=True)}", 1)
    
    atexit.register(cleanup_shared_memory, shared_mem)
    
    if not shared_mem.create(1):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        for widget in app.topLevelWidgets():
            if isinstance(widget, MainWindow):
                if widget.isMinimized():
                    widget.showNormal()
                widget.setWindowState(widget.windowState() & ~Qt.WindowMinimized)
                widget.activateWindow()
                widget.raise_()
                widget.show()
                return
        return
    
    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = resource_path(os.path.join("assets", "app.ico"))
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    
    ffmpeg_found, ffmpeg_path = check_ffmpeg()
    if not ffmpeg_found:
        print("FFmpeg not found. Please ensure it is installed and in PATH.")
    else:
        print(f"FFmpeg found at: {ffmpeg_path}")
    
    win = MainWindow(ffmpeg_found=ffmpeg_found, ffmpeg_path=ffmpeg_path)
    
    # Set window icon explicitly
    if os.path.exists(icon_path):
        win.setWindowIcon(app_icon)
    
    def cleanup():
        cleanup_shared_memory(shared_mem)
        if semaphore.acquire():
            semaphore.release()

    atexit.register(cleanup)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()