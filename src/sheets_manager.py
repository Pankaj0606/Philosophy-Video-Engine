"""
Google Sheets Manager:
Reads pending philosophy topics and updates completion status.
"""

import time
import sys
import gspread
from typing import Optional, Dict, Tuple


def connect_sheet():
    """Connects to the 'Philosophy_Videos' tab in DSA_Instagram_Automation."""
    for attempt in range(1, 4):
        try:
            gc = gspread.service_account(filename="config/credentials.json")
            sh = gc.open("DSA_Instagram_Automation")
            worksheet = sh.worksheet("Philosophy_Videos")
            return worksheet
        except Exception as e:
            print(f"⚠ Attempt {attempt}/3 connecting to Google Sheets failed: {e}")
            time.sleep(3)
    sys.exit("✗ Could not connect to Google Sheet. Check credentials and tab name.")


def get_next_pending_topic() -> Optional[Tuple[int, Dict]]:
    """Returns (row_number, topic_data) for the first pending row."""
    ws = connect_sheet()
    records = ws.get_all_records()

    for idx, r in enumerate(records):
        if str(r.get("Status", "")).strip().lower() == "pending":
            row_num = idx + 2
            return row_num, r
    return None


def mark_topic_completed(row_num: int):
    """Marks the given row as Completed in Google Sheets."""
    ws = connect_sheet()
    headers = ws.row_values(1)
    status_col = headers.index("Status") + 1
    ws.update_cell(row_num, status_col, "Completed")
    print(f"✓ Google Sheet row {row_num} marked as 'Completed'!")