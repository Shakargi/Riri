import os
from fastapi import APIRouter, UploadFile, File
from services.stt_service import convert_audio_to_text
from services.llm_service import generate_text

router = APIRouter()


@router.post("/audio", tags=["Chat"])
async def process_audio_message(file: UploadFile = File(...)):
    """
    מקבל קובץ אודיו, מתמלל אותו ושולח ל-Gemini.
    """
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        print("🎙️ ממיר אודיו לטקסט...")
        user_text = convert_audio_to_text(temp_file_path)

        print("🧠 חושב על תשובה...")
        ai_response = await generate_text(user_text)

        return {
            "status": "success",
            "user_text": user_text,
            "ai_response": ai_response
        }

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)