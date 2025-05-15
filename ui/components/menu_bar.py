from PySide6.QtWidgets import QMenuBar, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MenuBarManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_bar = None
        self.init_menu_bar()

    def init_menu_bar(self):
        self.menu_bar = self.main_window.menuBar()
        
        # File Menu
        file_menu = self.menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self.main_window)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.main_window.close)
        
        reset_profile_action = QAction("Reset Profile", self.main_window)
        reset_profile_action.triggered.connect(self.main_window.reset_profile)
        
        export_profile_action = QAction("Export Profile", self.main_window)
        export_profile_action.triggered.connect(self.main_window.profile_manager.export_profile)
        
        import_profile_action = QAction("Import Profile", self.main_window)
        import_profile_action.triggered.connect(self.main_window.profile_manager.import_profile)
        
        file_menu.addAction(exit_action)
        file_menu.addAction(reset_profile_action)
        file_menu.addAction(export_profile_action)
        file_menu.addAction(import_profile_action)
        
        
        help_menu = self.menu_bar.addMenu("Help")
        
        mail_action = QAction("Contact: toxi360@workmail.com", self.main_window)
        mail_action.triggered.connect(self.show_contact_info)
        
        github_action = QAction("Github: https://github.com/Efeckc17", self.main_window)
        github_action.triggered.connect(self.show_github_info)
        
        help_menu.addAction(mail_action)
        help_menu.addAction(github_action)

    def show_contact_info(self):
        QMessageBox.information(self.main_window, "Contact", "For support: toxi360@workmail.com")

    def show_github_info(self):
        QMessageBox.information(self.main_window, "GitHub", "https://github.com/Efeckc17")