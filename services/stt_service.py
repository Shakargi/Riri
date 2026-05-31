import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def convert_audio_to_text(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as audio_file:
        result = client.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1"
        )

    return result.text