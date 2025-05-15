import os

class ThemeManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.user_profile = main_window.user_profile
        self.current_theme = self.user_profile.get_theme()

    def get_dark_theme(self):
        css_path = os.path.join(os.path.dirname(__file__), "..", "themes", "dark.qss")
        with open(css_path, "r") as f:
            return f.read()

    def get_light_theme(self):
        css_path = os.path.join(os.path.dirname(__file__), "..", "themes", "light.qss")
        with open(css_path, "r") as f:
            return f.read()

    def get_current_theme_stylesheet(self):
        if self.current_theme == "Dark":
            return self.get_dark_theme()
        else:
            return self.get_light_theme()

    def apply_current_theme(self):
        self.main_window.setStyleSheet(self.get_current_theme_stylesheet())

    def change_theme(self, theme):
        self.user_profile.set_theme(theme)
        self.current_theme = theme
        self.apply_current_theme()
        self.main_window.append_log(f"Theme changed to '{theme}'.") 