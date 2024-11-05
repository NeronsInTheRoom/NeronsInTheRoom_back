from google.cloud import speech
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_PATH = os.getenv("googleSTT")

# Google Cloud 인증 설정
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

async def transcribe_audio(audio_content: bytes):
    
    # 인증된 클라이언트 생성
    client = speech.SpeechClient(credentials=credentials)
    
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="ko-KR",
    )
    
    response = client.recognize(config=config, audio=audio)
        
    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript + " "
        
    return transcribed_text.strip()
