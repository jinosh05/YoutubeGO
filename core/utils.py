from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

def apply_theme(app, theme):
    if theme == "Dark":
        stylesheet = """
        QMainWindow { background-color:#181818; border-radius:20px; }
        QLabel,QLineEdit,QPushButton,QListWidget,QTextEdit,QTableWidget,QComboBox,QCheckBox { color:#ffffff; background-color:#202020; border:none; border-radius:15px; }
        QLineEdit { border:2px solid #333; padding:8px; border-radius:15px; }
        QPushButton { background-color:#cc0000; padding:10px 16px; border-radius:15px; }
        QPushButton:hover { background-color:#b30000; }
        QListWidget::item { padding:12px; border-radius:10px; }
        QListWidget::item:selected { background-color:#333333; border-left:4px solid #cc0000; border-radius:10px; }
        QProgressBar { background-color:#333333; text-align:center; color:#ffffff; font-weight:bold; border-radius:15px; height:25px; }
        QProgressBar::chunk { background-color:#cc0000; border-radius:15px; }
        QMenuBar { background-color:#181818; color:#ffffff; border-radius:15px; }
        QMenuBar::item:selected { background-color:#333333; }
        QMenu { background-color:#202020; color:#ffffff; border-radius:15px; }
        QMenu::item:selected { background-color:#333333; }
        QTableWidget { gridline-color:#444444; border:2px solid #333; border-radius:15px; }
        QHeaderView::section { background-color:#333333; color:white; padding:6px; border:2px solid #444444; border-radius:8px; }
        QDockWidget { border:2px solid #333333; border-radius:15px; }
        """
    else:
        stylesheet = """
        QMainWindow { background-color:#f2f2f2; border-radius:20px; }
        QLabel,QLineEdit,QPushButton,QListWidget,QTextEdit,QTableWidget,QComboBox,QCheckBox { color:#000000; background-color:#ffffff; border:2px solid #ccc; border-radius:15px; }
        QLineEdit { border:2px solid #ccc; padding:8px; border-radius:15px; }
        QPushButton { background-color:#e0e0e0; padding:10px 16px; border-radius:15px; }
        QPushButton:hover { background-color:#cccccc; }
        QListWidget::item { padding:12px; border-radius:10px; }
        QListWidget::item:selected { background-color:#ddd; border-left:4px solid #888; border-radius:10px; }
        QProgressBar { background-color:#ddd; text-align:center; color:#000000; font-weight:bold; border-radius:15px; height:25px; }
        QProgressBar::chunk { background-color:#888; border-radius:15px; }
        QMenuBar { background-color:#ebebeb; color:#000; border-radius:15px; }
        QMenuBar::item:selected { background-color:#dcdcdc; }
        QMenu { background-color:#ffffff; color:#000000; border-radius:15px; }
        QMenu::item:selected { background-color:#dcdcdc; }
        QTableWidget { gridline-color:#ccc; border:2px solid #ccc; border-radius:15px; }
        QHeaderView::section { background-color:#f0f0f0; color:black; padding:6px; border:2px solid #ccc; border-radius:8px; }
        QDockWidget { border:2px solid #ccc; border-radius:15px; }
        """
    app.setStyleSheet(stylesheet)

def set_circular_pixmap(label, image_path):
    if image_path:
        pixmap = QPixmap(image_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        mask = QPixmap(50, 50)
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(0, 0, 50, 50)
        painter.end()
        pixmap.setMask(mask.createMaskFromColor(Qt.transparent))
        label.setPixmap(pixmap)
    else:
        label.setPixmap(QPixmap())

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
