# import os
# import sys
# import asyncio

# # MeloTTS 디렉토리를 Python 경로에 추가
# sys.path.append(os.path.abspath('MeloTTS'))
# from melo.api import TTS

# # TTS 모델 설정
# speed = 1.0
# device = 'cpu'  # 또는 'cuda:0'
# model = TTS(language='KR', device=device)

# async def generate_audio(text: str, filename: str):
#     # 오디오 파일을 저장할 디렉토리 설정
#     output_dir = 'static/audio'
#     os.makedirs(output_dir, exist_ok=True)

#     # 파일명이 .wav 확장자로 끝나도록 처리
#     if not filename.endswith('.wav'):
#         filename += '.wav'

#     # 파일 경로 구성
#     output_path = os.path.join(output_dir, filename)

#     try:
#         # TTS를 사용하여 오디오 파일 생성
#         speaker_ids = model.hps.data.spk2id
#         model.tts_to_file(text, speaker_ids['KR'], output_path, speed=speed)
#         return {"message": f"Success. {output_path}"}
#     except Exception as e:
#         return {"error": str(e)}