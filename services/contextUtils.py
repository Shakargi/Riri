import sqlite3
import json
import os
from datetime import datetime
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

    @staticmethod
    def save_message(role: str, content: str):
        ContextUtils._init_db() # מוודא שהטבלה קיימת
        with sqlite3.connect(ContextUtils.DB_NAME) as conn:
            conn.execute(
                "INSERT INTO conversation (role, content, timestamp) VALUES (?, ?, ?)",
                (role, content, datetime.now())
            )

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

    @staticmethod
    async def analyze_emotion(conversation_history: str) -> dict:
        prompt = f"""
        אתה מומחה לפסיכולוגיה. קרא את היסטוריית השיחה ונתח את המצב הרגשי.
        החזר JSON בלבד: {{"emotion": "...", "intensity": 1-10, "reasoning": "..."}}
        היסטוריית השיחה: {conversation_history}
        """
        try:
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_text)
        except Exception as e:
            return {"emotion": "ניטרלי", "intensity": 1, "reasoning": "שגיאה בניתוח."}