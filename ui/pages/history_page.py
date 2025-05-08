from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QHeaderView, 
                            QCheckBox, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.components.animated_button import AnimatedButton
from core.history import delete_selected_history, delete_all_history, search_history

class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
       
        lbl = QLabel("Download History")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Title","Channel","URL","Status"])
        hh = self.history_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        layout.addWidget(self.history_table)
        
        
        hl = QHBoxLayout()
        del_sel_btn = AnimatedButton("Delete Selected")
        del_sel_btn.clicked.connect(lambda: delete_selected_history(self.history_table, self.parent.append_log))
        del_all_btn = AnimatedButton("Delete All")
        del_all_btn.clicked.connect(lambda: delete_all_history(self.history_table, self.confirm_delete_all, self.parent.append_log))
        hist_ck = QCheckBox("Enable History Logging")
        hist_ck.setChecked(self.parent.user_profile.is_history_enabled())
        hist_ck.stateChanged.connect(self.toggle_history_logging)
        hl.addWidget(del_sel_btn)
        hl.addWidget(del_all_btn)
        hl.addWidget(hist_ck)
        layout.addLayout(hl)
        
        
        s_hl = QHBoxLayout()
        self.search_hist_edit = QLineEdit()
        self.search_hist_edit.setPlaceholderText("Search in history...")
        s_btn = AnimatedButton("Search")
        s_btn.clicked.connect(self.search_history_in_table)
        s_hl.addWidget(self.search_hist_edit)
        s_hl.addWidget(s_btn)
        layout.addLayout(s_hl)
        
        layout.addStretch()

    def toggle_history_logging(self, state):
        enabled = (state == Qt.Checked)
        self.parent.user_profile.set_history_enabled(enabled)
        self.parent.append_log(f"History logging {'enabled' if enabled else 'disabled'}.")

    def search_history_in_table(self):
        txt = self.search_hist_edit.text().lower().strip()
        search_history(self.history_table, txt)

    def confirm_delete_all(self):
        return self.parent.show_question("Delete All", "Are you sure?") 