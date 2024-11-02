from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from stt import transcribe_audio
from data import questions
from Q5 import Q5_score
from module.tts import generate_audio
from data import explanations
from data import scores

# 성우현
from module.Q1 import q1_evaluation
from module.Q2 import q2_evaluation
from module.Q3_qwen2 import hq3_qwen2_evaluation
from module.Q3 import q3_evaluation
from module.Q3_1 import q3_1_evaluation
from module.Q8 import q8_evaluation
from module.Q8_qwen2 import q8_qwen2_evaluation
from module.Q9 import q9_evaluation
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    correctAnswer = "93"
    score = await Q5_score(text, correctAnswer)
        
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q5-2")
async def speech_to_text(file: UploadFile = File(...)):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    correctAnswer = "86"
    score = await Q5_score(text, correctAnswer)
        
    return {
        "score": score,
        "answer": text  
    }
  
# 사용시에만 주석제거
# @app.post("/tts")
# async def generate_audio(text: str, filename: str):
#     result = generate_audio(text=text, filename=filename)
#     return result

@app.post("/Q1")
async def speech_to_text(birth_date: str=Form(...), file: UploadFile = File(...)):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    
    score = await q1_evaluation(birth_date, text)
    
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q2")
async def speech_to_text(file: UploadFile = File(...)):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    
    score = await q2_evaluation(text)
    
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q3")
async def speech_to_text(location: str=Form(...), file: UploadFile = File(...)):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    
    try:
        # 5초 내에 q3_evaluation 함수 호출
        score = await asyncio.wait_for(q3_evaluation(location, text), timeout=5)
        # score가 -1인 경우 Q3-1로 리디렉션 ("모르겠다"와 같은 의미)
        if score == -1:
            response = await speech_to_text_alternate(location, file)
    except asyncio.TimeoutError:
        # 5초 초과 시 Q3-1로 리디렉션
        response = await speech_to_text_alternate(location, file)
        return response
    
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q3-1")
async def speech_to_text_alternate(location: str=Form(...), file: UploadFile = File(...)):    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    
    score = await q3_1_evaluation(location, text)
    
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q8")
async def speech_to_text(file: UploadFile = File(...)):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    
    score = await q8_evaluation(text)
    
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q9")
async def speech_to_text(file: UploadFile = File(...)):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    
    score = await q9_evaluation(text)
    
    return {
        "score": score,
        "answer": text  
    }

# @app.post("/Q1")
# async def q1(age: str=Form(...), answer: str=Form(...)):
#     return q1_evaluation(age, answer)

# @app.post("/Q2")
# async def q2(answer: str=Form(...)):
#     return q2_evaluation(answer)

# @app.post("/Q3")
# async def q3(location: str=Form(...), answer: str=Form(...)):
#     return q3_evaluation(location, answer)

# @app.post("/Q8")
# async def q8(answer: str=Form(...)):
#     return q8_evaluation(answer)

# @app.post("/Q9")
# async def q9(answer: str=Form(...)):
#     return q9_evaluation(answer)
 
# 데이터 전달
@app.get("/get_explanations")
async def get_explanations(): return explanations

@app.get("/get_scores")
async def get_scores(): return scores
