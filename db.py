# db.py
import sqlite3

CONN = sqlite3.connect('company.db')  # Use a file-based database
CURSOR = CONN.cursor()
CURSOR.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
CONN.commit()