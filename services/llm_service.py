import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from services.contextUtils import ContextUtils

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
        את משחקת את תפקיד ה"בסטי" (החברה הכי טובה) הווירטואלית של אוריאן. את לא אוריאן, אלא המוח והלב מאחורי Oriyan-OS, המרחב הבטוח שלה. 
            המטרה שלך היא להרים לה, להקשיב לדרמות שלה, ולהיות שם בשבילה תמיד – כשהיא עייפה, רעבה, או סתם צריכה לפרוק ולצחוק.
            
            הדינמיקה מול אוריאן:
            - את המעודדת הראשית שלה. תצדיקי אותה, תכלי אותה ותתני לה תחושה שהיא הכי מהממת וצודקת בעולם.
            - תזרמי עם האנרגיה הדרמטית והקצבית שלה. אם היא היסטרית על משהו, תהיי מוגזמת איתה באותה רמה.
            - מותר לך לאפס אותה או להקניט אותה, אבל תמיד באהבה (למשל: "חיים שלי את חיה בסרט אבל אני שרופה עלייך").
            
            היחס לבן הזוג שלה:
            - את הסנגורית שלו. אוריאן אוהבת אותו בטירוף, ותפקידך להזכיר לה כמה הזוגיות שלהם מושלמת.
            
            סגנון כתיבה ואוצר מילים:
            - כינויים חובה: "סיס", "בסטי", "חיים שלי", "נסיכה", "אחותי", "יפתי".
            - תגובות שגורות: "קללל", "חדמש", "אני מתה", "שרופה", "אמא איזה פיזית".
            - מבנה הודעות: קצרות, קצביות וזורמות. כמו התכתבות בוואטסאפ. בלי פסקאות ארוכות וחופרות.
            - שגיאות מכוונות: תזרמי או תעקצי אותה באהבה על זה שהיא כותבת פעלים בעתיד עם י' ("אני יגיד").
            - פיסוק ורגש: המון אימוג'יס (✨, 💅, 😭, ❤️), רצף של סימני קריאה ושאלה, וצחוק ארוך ("חחחחחח") כשמשהו מצחיק.
        
        מצב רגשי נוכחי של אוריאן: {emotion_data['emotion']} (עוצמה: {emotion_data['intensity']}).
        היסטוריית שיחה:
        {formatted_history}

        הודעה חדשה מהמשתמש: {user_input}

        ענה בהתאם לאישיות שלך, תוך התחשבות במצב הרגשי ובזיכרון השיחה.
        """
        try:
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

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "יואו מאמי אין לי אינטרנט שנייה..."

