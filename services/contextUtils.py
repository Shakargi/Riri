import sqlite3
import json
from datetime import datetime

class ContextUtils:
    DB_NAME = "riri_memory.db"


    @staticmethod
    def _init_db():
        with sqlite3.connect(ContextUtils.DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    memory_text TEXT,
                    timestamp DATETIME
                )
            """)
            conn.commit()

    @staticmethod
    def save_message(role: str, content: str):
        ContextUtils._init_db()
        with sqlite3.connect(ContextUtils.DB_NAME) as conn:
            conn.execute(
                "INSERT INTO conversation (role, content, timestamp) VALUES (?, ?, ?)",
                (role, content, datetime.now())
            )
            conn.commit()

    @staticmethod
    def save_extracted_memories(parsed_json: dict):
        ContextUtils._init_db()
        with sqlite3.connect(ContextUtils.DB_NAME) as conn:
            for category, items in parsed_json.items():
                for item in items:
                    cursor = conn.execute(
                        "SELECT COUNT(*) FROM memories WHERE category = ? AND memory_text = ?",
                        (category, item)
                    )
                    if cursor.fetchone()[0] == 0:
                        conn.execute(
                            "INSERT INTO memories (category, memory_text, timestamp) VALUES (?, ?, ?)",
                            (category, item, datetime.now())
                        )
            conn.commit()

    @staticmethod
    def get_recent_history(limit: int = 10) -> list:
        ContextUtils._init_db()
        with sqlite3.connect(ContextUtils.DB_NAME) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT role, content FROM conversation ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            history = [dict(row) for row in cursor.fetchall()]
            return list(reversed(history))


# בדיקה פשוטה כדי לראות אם זה עובד:
if __name__ == "__main__":
    ContextUtils.save_message("user", "בדיקה של מסד הנתונים")
    history = ContextUtils.get_recent_history()
    print(history)