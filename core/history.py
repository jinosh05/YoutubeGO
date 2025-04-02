import os
import json
from PyQt5.QtWidgets import QTableWidgetItem

HISTORY_FILE = "history.json"

def load_history_initial(table):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f, indent=4)
    else:
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
                for entry in history:
                    row = table.rowCount()
                    table.insertRow(row)
                    table.setItem(row, 0, QTableWidgetItem(entry.get("title", "")))
                    table.setItem(row, 1, QTableWidgetItem(entry.get("channel", "")))
                    table.setItem(row, 2, QTableWidgetItem(entry.get("url", "")))
                    table.setItem(row, 3, QTableWidgetItem(entry.get("status", "")))
        except:
            pass

def save_history(table):
    history = []
    for r in range(table.rowCount()):
        title = table.item(r,0).text() if table.item(r,0) else ""
        channel = table.item(r,1).text() if table.item(r,1) else ""
        url = table.item(r,2).text() if table.item(r,2) else ""
        status = table.item(r,3).text() if table.item(r,3) else ""
        history.append({"title": title, "channel": channel, "url": url, "status": status})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def add_history_entry(table, title, channel, url, status, enabled=True):
    if not enabled:
        return
    row = table.rowCount()
    table.insertRow(row)
    table.setItem(row, 0, QTableWidgetItem(title))
    table.setItem(row, 1, QTableWidgetItem(channel))
    table.setItem(row, 2, QTableWidgetItem(url))
    table.setItem(row, 3, QTableWidgetItem(status))
    save_history(table)

def delete_selected_history(table, log_callback):
    selected_rows = set()
    for it in table.selectedItems():
        selected_rows.add(it.row())
    for r in sorted(selected_rows, reverse=True):
        table.removeRow(r)
    log_callback(f"Deleted {len(selected_rows)} history entries.")
    save_history(table)

def delete_all_history(table, confirm, log_callback):
    ans = confirm()
    if ans:
        table.setRowCount(0)
        log_callback("All history deleted.")
        save_history(table)

def search_history(table, txt):
    for r in range(table.rowCount()):
        hide = True
        for c in range(table.columnCount()):
            it = table.item(r, c)
            if it and txt in it.text().lower():
                hide = False
                break
        table.setRowHidden(r, hide)
