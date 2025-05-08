from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QFormLayout, QLineEdit, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from ui.components.animated_button import AnimatedButton
import os

class ProfilePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        
        lbl = QLabel("Profile Page - Customize your details")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        
       
        form_layout = QFormLayout()
        
       
        self.profile_name_edit = QLineEdit()
        self.profile_name_edit.setText(self.parent.user_profile.data["name"])
        form_layout.addRow("Name:", self.profile_name_edit)
        
        
        self.pic_label = QLabel("No file selected.")
        if self.parent.user_profile.data["profile_picture"]:
            self.pic_label.setText(os.path.basename(self.parent.user_profile.data["profile_picture"]))
        
        pic_btn = AnimatedButton("Change Picture")
        self.remove_pic_btn = AnimatedButton("Remove Picture")
        self.remove_pic_btn.setVisible(bool(self.parent.user_profile.data["profile_picture"]))
        
        pic_btn.clicked.connect(self.pick_pic)
        self.remove_pic_btn.clicked.connect(self.remove_pic)
        
        form_layout.addRow("Picture:", pic_btn)
        form_layout.addRow(self.pic_label)
        form_layout.addRow(self.remove_pic_btn)
        
        
        self.insta_edit = QLineEdit()
        self.insta_edit.setText(self.parent.user_profile.data["social_media_links"].get("instagram",""))
        form_layout.addRow("Instagram:", self.insta_edit)
        
        self.tw_edit = QLineEdit()
        self.tw_edit.setText(self.parent.user_profile.data["social_media_links"].get("twitter",""))
        form_layout.addRow("Twitter:", self.tw_edit)
        
        self.yt_edit = QLineEdit()
        self.yt_edit.setText(self.parent.user_profile.data["social_media_links"].get("youtube",""))
        form_layout.addRow("YouTube:", self.yt_edit)
        
        layout.addLayout(form_layout)
        
        
        save_btn = AnimatedButton("Save Profile")
        save_btn.clicked.connect(self.save_profile)
        layout.addWidget(save_btn)
        
        layout.addStretch()

    def pick_pic(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.pic_label.setText(os.path.basename(path))
            self.pic_label.setProperty("selected_path", path)
            self.remove_pic_btn.setVisible(True)

    def remove_pic(self):
        self.parent.user_profile.remove_profile_picture()
        self.pic_label.setText("No file selected.")
        self.pic_label.setProperty("selected_path", "")
        self.remove_pic_btn.setVisible(False)
        self.parent.profile_pic_label.setPixmap(QPixmap())
        self.parent.profile_name_label.setText("User")

    def save_profile(self):
        name = self.profile_name_edit.text().strip()
        if not name:
            self.parent.show_warning("Error", "Please provide a name.")
            return
            
        pic_path = self.pic_label.property("selected_path") if self.pic_label.property("selected_path") else self.parent.user_profile.data["profile_picture"]
        
        self.parent.user_profile.set_profile(
            name, 
            pic_path, 
            self.parent.user_profile.get_download_path()
        )
        
        self.parent.user_profile.set_social_media_links(
            self.insta_edit.text().strip(),
            self.tw_edit.text().strip(),
            self.yt_edit.text().strip()
        )
        
        self.parent.update_profile_ui()
        self.parent.show_info("Success", "Profile settings saved successfully.") 