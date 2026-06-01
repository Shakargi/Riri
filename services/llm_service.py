import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from Riri.services.contextUtils import ContextUtils

load_dotenv()


class LLMService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-2.5-flash"
        self.system_prompt = "..."

    async def generate_response(self, user_input: str) -> str:
        ContextUtils.save_message("user", user_input)

        history = ContextUtils.get_recent_history(limit=10)
        formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

        emotion_data = await ContextUtils.analyze_emotion(formatted_history)

        full_prompt = f"""
        מצב רגשי נוכחי של אוריאן: {emotion_data['emotion']} (עוצמה: {emotion_data['intensity']}).
        היסטוריית שיחה:
        {formatted_history}

        הודעה חדשה מהמשתמש: {user_input}

        ענה בהתאם לאישיות שלך, תוך התחשבות במצב הרגשי ובזיכרון השיחה.
        """

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt
            )
        )

        answer = response.text

        ContextUtils.save_message("riri", answer)

        return answer