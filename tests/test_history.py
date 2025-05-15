from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
import pytest
from core.history import (
    load_history_initial,
    save_history,
    add_history_entry,
    delete_selected_history,
    delete_all_history,
    search_history,
    export_history
)
import json
import os

@pytest.fixture
def history_table(qapp):
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Title", "Channel", "URL", "Status"])
    return table

@pytest.fixture
def sample_history_data():
    return [
        {"title": "Test Video 1", "channel": "Channel 1", "url": "https://youtube.com/1", "status": "Completed", "date": "2024-01-01"},
        {"title": "Test Video 2", "channel": "Channel 2", "url": "https://youtube.com/2", "status": "Failed", "date": "2024-01-02"},
        {"title": "Test Video 3", "channel": "Channel 3", "url": "https://youtube.com/3", "status": "Completed", "date": "2024-01-03"}
    ]

def test_add_history_entry(history_table):
    add_history_entry(
        history_table,
        "Test Video",
        "Test Channel",
        "https://youtube.com/test",
        "Completed",
        True
    )
    
    assert history_table.rowCount() == 1
    assert history_table.item(0, 0).text() == "Test Video"
    assert history_table.item(0, 1).text() == "Test Channel"
    assert history_table.item(0, 2).text() == "https://youtube.com/test"
    assert history_table.item(0, 3).text() == "Completed"

def test_save_and_load_history(history_table, temp_data_dir, sample_history_data):
    for entry in sample_history_data:
        add_history_entry(
            history_table,
            entry["title"],
            entry["channel"],
            entry["url"],
            entry["status"],
            True
        )
    
    save_history(history_table)
    
    history_table.setRowCount(0)
    assert history_table.rowCount() == 0
    
    load_history_initial(history_table)
    
    assert history_table.rowCount() == len(sample_history_data)
    for i, entry in enumerate(sample_history_data):
        assert history_table.item(i, 0).text() == entry["title"]
        assert history_table.item(i, 1).text() == entry["channel"]
        assert history_table.item(i, 2).text() == entry["url"]
        assert history_table.item(i, 3).text() == entry["status"]

def test_delete_selected_history(history_table, sample_history_data):
    for entry in sample_history_data:
        add_history_entry(
            history_table,
            entry["title"],
            entry["channel"],
            entry["url"],
            entry["status"],
            True
        )
    
    history_table.setSelectionMode(QTableWidget.MultiSelection)
    history_table.selectRow(0)
    history_table.selectRow(2)
    
    def mock_log(msg):
        pass
    
    delete_selected_history(history_table, mock_log)
    
    assert history_table.rowCount() == 1
    assert history_table.item(0, 0).text() == sample_history_data[1]["title"]

def test_delete_all_history(history_table, sample_history_data):
    for entry in sample_history_data:
        add_history_entry(
            history_table,
            entry["title"],
            entry["channel"],
            entry["url"],
            entry["status"],
            True
        )
    
    initial_count = history_table.rowCount()
    assert initial_count > 0
    
    def mock_confirm():
        return True
    def mock_log(msg):
        pass
    
    delete_all_history(history_table, mock_confirm, mock_log)
    assert history_table.rowCount() == 0

def test_search_history(history_table, sample_history_data):
    for entry in sample_history_data:
        add_history_entry(
            history_table,
            entry["title"],
            entry["channel"],
            entry["url"],
            entry["status"],
            True
        )
    
    search_history(history_table, "Test Video 1")
    visible_rows = sum(1 for row in range(history_table.rowCount()) 
                      if not history_table.isRowHidden(row))
    assert visible_rows == 1
    
    search_history(history_table, "")
    visible_rows = sum(1 for row in range(history_table.rowCount()) 
                      if not history_table.isRowHidden(row))
    assert visible_rows == len(sample_history_data)
    
    search_history(history_table, "Channel")
    visible_rows = sum(1 for row in range(history_table.rowCount()) 
                      if not history_table.isRowHidden(row))
    assert visible_rows == len(sample_history_data)
    
    search_history(history_table, "NonExistent")
    visible_rows = sum(1 for row in range(history_table.rowCount()) 
                      if not history_table.isRowHidden(row))
    assert visible_rows == 0

def test_export_history(history_table, temp_data_dir, sample_history_data):
    for entry in sample_history_data:
        add_history_entry(
            history_table,
            entry["title"],
            entry["channel"],
            entry["url"],
            entry["status"],
            True
        )
    
    export_file = os.path.join(temp_data_dir, "history_export.json")
    export_history(export_file)
    
    assert os.path.exists(export_file)
    
    with open(export_file, 'r') as f:
        exported_data = json.load(f)
    
    assert len(exported_data) == len(sample_history_data)
    for i, entry in enumerate(exported_data):
        assert entry["title"] == sample_history_data[i]["title"]
        assert entry["channel"] == sample_history_data[i]["channel"]
        assert entry["url"] == sample_history_data[i]["url"]
        assert entry["status"] == sample_history_data[i]["status"]
