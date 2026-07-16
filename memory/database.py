import sqlite3
import os

DB_PATH = "database/assistant.db"


def initialize_database():
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Conversations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        assistant TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Memories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memory_key TEXT UNIQUE,
        memory_value TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized.")