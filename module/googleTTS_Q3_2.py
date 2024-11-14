import os
from google.cloud import texttospeech
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()
CREDENTIALS_PATH = os.getenv("googleTTS") 
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

async def generate_Q3_2(text: str):
    filename = "Q3-2"
    output_dir = 'static/temp'
    os.makedirs(output_dir, exist_ok=True)

    if not filename.endswith('.wav'):
        filename += '.wav'

    output_path = os.path.join(output_dir, filename)

    try:
        # 인증된 클라이언트 생성
        client = texttospeech.TextToSpeechClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Standard-B",  # 여성 목소리
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=1.0,
            pitch=0.0,
        )

        response = client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            
        return {"message": f"Q3-1 오디오 생성 성공"}
    except Exception as e:
        return {"error": str(e)}