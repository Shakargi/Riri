import os
import sqlite3
from datetime import datetime
from services.llm_service import LLMService
import json

class MemoryService:
    def __init__(self):
        BASE_DIR = os.getcwd()
        db_name = os.path.join(BASE_DIR, "riri_memory.db")

        self.db_name = db_name
        self._init_db()
        self.llm = LLMService()
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

    def get_recent_history(self, limit: int = 2) -> list:
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT role, content FROM conversation ORDER BY id DESC LIMIT ?",
                (limit,)
            )
            history = [dict(row) for row in cursor.fetchall()]
            return list(reversed(history))

    import json

    async def get_important_memories(self):
        history = self.get_recent_history()

        full_prompt = f"""
    You are an intelligent data extraction module. Your task is to analyze the following chat history and extract the most recent and important context about the user. 
    This data will be used to populate a frontend dashboard and must be saved into an SQLite database.

    <chat_history>
    {history}
    </chat_history>

    Extract the information into the following strictly structured JSON format. 
    Rules:
    1. ONLY output valid JSON. Do not include markdown tags like ```json or any conversational text before or after the JSON object.
    2. If a category has no new information, return an empty array [] for that key.
    3. Be concise and capture the core meaning. Do not hallucinate or guess.

    {{
      "recent_events": [
      ],
      "preferences_and_likes": [
      ],
      "current_mood_or_state": [
      ],
      "important_reminders": [
      ]
    }}
    """

        raw_response = await self.llm.get_answer(full_prompt=full_prompt)
        try:
            parsed_json = json.loads(raw_response)
            return parsed_json
        except json.JSONDecodeError:
            print("[Memory Service] Error: LLM did not return valid JSON.")
            return raw_response





