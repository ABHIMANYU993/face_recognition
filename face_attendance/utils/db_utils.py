# utils/db_utils.py
import os
import sqlite3


def create_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/students.db")
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
