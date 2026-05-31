import os
import json
from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class EmotionService:
    def __init__(self):
        self.model_name = "gemini-2.5-flash"


    async def analyze_emotion(self, conversation_history: str) -> dict:
        prompt = f"""
        אתה מומחה לפסיכולוגיה ואינטליגנציה רגשית.
        קרא את היסטוריית השיחה הבאה עם אוריאן, ונתח את המצב הרגשי שלה כרגע.
        עליך להחזיר את התשובה בפורמט JSON חוקי בלבד (ללא טקסט נוסף וללא markdown), עם השדות הבאים:
        - "emotion": הרגש המרכזי שזיהית (למשל: שמחה, לחץ, עייפות, תסכול, רוגע, התלהבות, עצבות).
        - "intensity": מספר שלם מ-1 עד 10 המייצג את עוצמת הרגש.
        - "reasoning": משפט קצר אחד שמסביר מתוך הטקסט למה זה הרגש שזוהה.

        היסטוריית השיחה:
        {conversation_history}
        """

        try:
            print("[Emotion Service] Analyzing current emotional state...")
            response = await client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            raw_text = response.text.strip()

            if raw_text.startswith("```json"):
                raw_text = raw_text[7:-3].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:-3].strip()

            emotion_data = json.loads(raw_text)
            print(
                f"[Emotion Service] Detected Emotion: {emotion_data.get('emotion')} (Level {emotion_data.get('intensity')})")

            return emotion_data

        except Exception as e:
            print(f"[Emotion Service] Error analyzing emotion: {e}")
            return {"emotion": "ניטרלי", "intensity": 1, "reasoning": "שגיאה בניתוח הרגש."}
