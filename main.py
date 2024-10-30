from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from module.tts import generate_audio

# 성우현
from module.uh_q1 import hq1_evaluation
from module.uh_q2 import hq2_evaluation

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

@app.post("/hq1")
async def hq1(age: str=Form(...), answer: str=Form(...)):
    return  hq1_evaluation(age, answer)

@app.post("/hq2")
async def hq2(answer: str=Form(...)):
    return hq2_evaluation(answer)