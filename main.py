from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from stt import transcribe_audio
from data import questions
from Q5 import Q5_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 도메인
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start")
async def get_questions():
    try:
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 목록을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )

@app.post("/Q5-1")
async def speech_to_text(file: UploadFile = File(...)):
    
    # 파일 확장자 확인
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    # 파일 컨텐츠 읽기
    contents = await file.read()
        
    # STT 처리
    text = await transcribe_audio(contents)

    correctAnswer = "93"

    score = await Q5_score(text, correctAnswer)
        
    return {"score" : score}


@app.post("/Q5-2")
async def speech_to_text(file: UploadFile = File(...)):
    
    # 파일 확장자 확인
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    # 파일 컨텐츠 읽기
    contents = await file.read()
        
    # STT 처리
    text = await transcribe_audio(contents)

    correctAnswer = "86"

    score = await Q5_score(text, correctAnswer)
        
    return {"score" : score}