import os
import edge_tts
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
class TTSService:
    def __init__(self):
        self.voice = "he-IL-HilaNeural"

    async def format_text_for_tts(self, original_text: str) -> str:
        prompt = f"""
        אתה מומחה לבלשנות ולמערכות Text-to-Speech בעברית.
        המטרה שלך היא לקחת את הטקסט הבא, ולשכתב אותו כך שמנוע הקראה (TTS) יקרא אותו בצורה הכי טבעית, אנושית וזורמת שאפשר.
        - תקן מילים מוגזמות (למשל הפוך "איממממאאאאא" ל-"אִמָּא").
        - הוסף פסיקים ונקודות כדי לייצר נשימות והפסקות טבעיות.
        - הוסף ניקוד חלקי למילים שעלולות להיות דו-משמעיות או שקשות להגייה למנוע.
        - שמור בדיוק על המשמעות והתוכן המקורי, אל תוסיף מילים משלך.

        הטקסט המקורי:
        {original_text}

        החזר אך ורק את הטקסט המוכן להקראה, ללא שום תוספות.
        """

        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()

    async def synthesize_speech(self, text: str, output_filename: str = "output_audio.mp3") -> str:
        try:
            print(f"[TTS Service] Original text: '{text}'")

            ready_for_speech_text = await self.format_text_for_tts(text)
            print(f"[TTS Service] Formatted text for TTS: '{ready_for_speech_text}'")

            communicate = edge_tts.Communicate(ready_for_speech_text, self.voice, rate="-10%")

            await communicate.save(output_filename)

            print(f"[TTS Service] Successfully saved audio to {output_filename}")
            return output_filename

        except Exception as e:
            print(f"[TTS Service] Exception occurred: {e}")
            return None

