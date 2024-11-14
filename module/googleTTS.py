import os
from google.cloud import texttospeech
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()
CREDENTIALS_PATH = os.getenv("googleTTS")
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

async def generate_audio(text: str, filename: str):
    # 오디오 파일을 저장할 디렉토리 설정
    output_dir = 'static/audio'
    os.makedirs(output_dir, exist_ok=True)

    # 파일명이 .wav 확장자로 끝나도록 처리
    if not filename.endswith('.wav'):
        filename += '.wav'

    # 파일 경로 구성
    output_path = os.path.join(output_dir, filename)

    try:
        # 인증된 클라이언트 생성
        client = texttospeech.TextToSpeechClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR",
            name="ko-KR-Standard-B",  # 남성 목소리
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

        return {"message": f"Success. {output_path}"}
    except Exception as e:
        return {"error": str(e)}