import os
import base64
import shutil
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File

from services.llm_service import LLMService
from services.tts_service import synthesize_speech
from services.stt_service import convert_audio_to_text

router = APIRouter()
llm = LLMService()

class TextRequest(BaseModel):
    text: str

@router.post("/text")
async def process_text(request: TextRequest):
    ai_response = await llm.generate_response(request.text)
    return {"status": "success", "user_text": request.text, "response": ai_response}


@router.post("/audio")
async def chat_audio(file: UploadFile = File(...)):
    temp_input_path = f"temp_in_{file.filename}"
    temp_output_path = f"temp_out_{file.filename}.mp3"

    try:
        with open(temp_input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        user_text = convert_audio_to_text(temp_input_path)

        riri_text = await llm.generate_response(user_text)

        await synthesize_speech(riri_text, temp_output_path)

        audio_base64 = ""
        if os.path.exists(temp_output_path):
            with open(temp_output_path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

        return {
            "status": "success",
            "user_text": user_text,
            "riri_response": riri_text,
            "audio_base64": audio_base64
        }

    finally:
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)