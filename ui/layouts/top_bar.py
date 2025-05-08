from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QListWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.components.animated_button import AnimatedButton
from core.utils import set_circular_pixmap

class TopBarLayout:
    def __init__(self, parent):
        self.parent = parent
        self.container = QWidget()
        self.container.setMinimumHeight(100)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        
        
        profile_container = QVBoxLayout()
        self.profile_pic_label = QLabel()
        self.profile_pic_label.setFixedSize(50, 50)
        set_circular_pixmap(self.profile_pic_label, self.parent.user_profile.data["profile_picture"])
        
        self.profile_name_label = QLabel(self.parent.user_profile.data["name"] if self.parent.user_profile.data["name"] else "User")
        self.profile_name_label.setFont(QFont("Arial", 10))
        
        profile_container.addWidget(self.profile_pic_label, alignment=Qt.AlignCenter)
        profile_container.addWidget(self.profile_name_label, alignment=Qt.AlignCenter)
        
        profile_widget = QWidget()
        profile_widget.setLayout(profile_container)
        
        
        pref_string = (f"Resolution: {self.parent.user_profile.get_default_resolution()}\n"
                      f"Theme: {self.parent.user_profile.get_theme()}\n"
                      f"Download Path: {self.parent.user_profile.get_download_path()}\n"
                      f"Proxy: {self.parent.user_profile.get_proxy()}\n")
        profile_widget.setToolTip(pref_string)
        
        layout.addWidget(profile_widget, alignment=Qt.AlignLeft)
        
        
        self.logo_label = QLabel("YoutubeGO 4.4")
        self.logo_label.setFont(QFont("Arial", 22, QFont.Bold))
        layout.addWidget(self.logo_label, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        
        
        search_container = QWidget()
        sc_layout = QHBoxLayout(search_container)
        sc_layout.setSpacing(10)
        sc_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search in app...")
        self.search_edit.setFixedHeight(40)
        
        self.search_btn = AnimatedButton("Search")
        self.search_btn.setFixedHeight(40)
        self.search_btn.clicked.connect(self.parent.top_search_clicked)
        
        sc_layout.addWidget(self.search_edit)
        sc_layout.addWidget(self.search_btn)
        
        layout.addWidget(search_container, stretch=1, alignment=Qt.AlignVCenter)
        
        # Search Results List
        self.search_result_list = QListWidget()
        self.search_result_list.setVisible(False)
        self.search_result_list.setFixedHeight(250)
        self.search_result_list.itemClicked.connect(self.parent.search_item_clicked) 