import sqlite3
from datetime import datetime


class MemoryService:
    def __init__(self, db_name="riri_memory.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME
                )
            """)

    def save_message(self, role: str, content: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO conversation (role, content, timestamp) VALUES (?, ?, ?)",
                (role, content, datetime.now())
            )

    def get_recent_history(self, limit: int = 10) -> list:
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT role, content FROM conversation ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            history = [dict(row) for row in cursor.fetchall()]
            return list(reversed(history))


