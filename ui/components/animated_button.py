from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class AnimatedButton(QPushButton):
    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
            QPushButton:pressed {
                background-color: #cc3333;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)
        super().leaveEvent(event) 