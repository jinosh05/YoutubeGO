from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
import os
import sys
from pathlib import Path


def set_circular_pixmap(label, image_path):
    if not image_path:
        label.setPixmap(QPixmap())
        return

    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        label.setPixmap(QPixmap())
        return

    scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    mask = QPixmap(scaled_pixmap.size())
    mask.fill(Qt.transparent)
    
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QBrush(Qt.white))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
    painter.end()
    
    scaled_pixmap.setMask(mask.createMaskFromColor(Qt.transparent))
    label.setPixmap(scaled_pixmap)

def format_speed(speed):
    if speed > 1000000:
        return f"{speed / 1000000:.2f} MB/s"
    elif speed > 1000:
        return f"{speed / 1000:.2f} KB/s"
    else:
        return f"{speed} B/s"

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{int(h)}h {int(m)}m {int(s)}s"
    elif m:
        return f"{int(m)}m {int(s)}s"
    else:
        return f"{int(s)}s"

def get_data_dir():
    """
    Get the application data directory path.
    On Windows: %APPDATA%/YoutubeGO
    On Linux: ~/.local/share/youtubego
    On macOS: ~/Library/Application Support/YoutubeGO
    """
    if sys.platform == 'win32':
        base_dir = os.getenv('APPDATA')
    elif sys.platform == 'darwin':
        base_dir = os.path.expanduser('~/Library/Application Support')
    else:  
        base_dir = os.path.expanduser('~/.local/share')

    data_dir = os.path.join(base_dir, 'YoutubeGO')
    os.makedirs(data_dir, exist_ok=True)

    # Create subdirectories
    images_dir = os.path.join(data_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    return data_dir

def get_images_dir():
    """Get the directory path for profile images."""
    return os.path.join(get_data_dir(), 'images')
