import unittest
from core.history import save_history, load_history_initial, add_history_entry
from PyQt5.QtWidgets import QApplication, QTableWidget
import os
import sys

app = QApplication(sys.argv)

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.table = QTableWidget()
        self.test_file = "history.json"

    def test_add_history_entry(self):
        add_history_entry(self.table, "Title", "Channel", "URL", "Status", enabled=True)
        self.assertEqual(self.table.rowCount(), 1)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == "__main__":
    unittest.main()
