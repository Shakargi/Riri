import os
import edge_tts
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def synthesize_speech(text: str, output_filename: str, voice: str = "he-IL-HilaNeural") -> str:
    try:
        prompt = f"""
        אתה מומחה לבלשנות ולמערכות Text-to-Speech בעברית.
        המטרה שלך היא לקחת את הטקסט הבא, ולשכתב אותו כך שמנוע הקראה (TTS) יקרא אותו בצורה הכי טבעית, אנושית וזורמת שאפשר.
        - תקן מילים מוגזמות (למשל הפוך "איממממאאאאא" ל-"אִמָּא").
        - הוסף פסיקים ונקודות כדי לייצר נשימות והפסקות טבעיות.
        - הוסף ניקוד חלקי למילים שעלולות להיות דו-משמעיות או שקשות להגייה למנוע.
        - שמור בדיוק על המשמעות והתוכן המקורי, אל תוסיף מילים משלך.

        הטקסט המקורי:
        {text}

        החזר אך ורק את הטקסט המוכן להקראה, ללא שום תוספות.
        """

        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        ready_for_speech_text = response.text.strip()

        communicate = edge_tts.Communicate(ready_for_speech_text, voice, rate="-10%")
        await communicate.save(output_filename)

        return output_filename

    except Exception:
        return None