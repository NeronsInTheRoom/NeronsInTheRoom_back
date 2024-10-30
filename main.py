from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from module.tts import generate_audio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 사용시에만 주석제거
# @app.post("/tts")
# async def create_audio(text: str, filename: str):
#     result = generate_audio(text=text, filename=filename)
#     return result