# utils/db_utils.py
import os
import sqlite3


def get_db_path():
    # Dynamically resolve database path relative to this file's folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, "database")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "students.db")


def create_db():
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        embedding BLOB NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS attendance (
        id TEXT,
        name TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()
