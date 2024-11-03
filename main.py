from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from stt import transcribe_audio
from data import questions
from data import answers
from Q4andQ7 import Q4AndQ7Score
from Q5andQ6 import Q5AndQ6Score
# from module.tts import generate_audio
from data import explanations
from data import scores

# 성우현
from module.uh_q1 import hq1_evaluation
from module.uh_q2 import hq2_evaluation
from module.uh_q9 import hq9_evaluation

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
        return {"questions": questions, "answers": answers}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"질문 목록을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )
    
# Q4, Q7 스코어 계산
async def Q4andQ7(file: UploadFile, correctAnswer: str):

    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    correctAnswer = correctAnswer
    score = await Q4AndQ7Score(text, correctAnswer)
        
    return {
        "score": score,
        "answer": text  
    }

# Q5, Q6 스코어 계산
async def Q5andQ6(file: UploadFile, correctAnswer: str):
    
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
        
    text = await transcribe_audio(contents)
    correctAnswer = correctAnswer
    score = await Q5AndQ6Score(text, correctAnswer)
        
    return {
        "score": score,
        "answer": text  
    }
    
@app.post("/Q4")
async def speech_to_text_q4(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q4andQ7(file, correctAnswer)


@app.post("/Q5")
async def speech_to_text_q5(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q5andQ6(file, correctAnswer)
    

@app.post("/Q5-1")
async def speech_to_text_q5(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q5andQ6(file, correctAnswer)

@app.post("/Q6")
async def speech_to_text_q5(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q5andQ6(file, correctAnswer)

@app.post("/Q6-1")
async def speech_to_text_q5(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q5andQ6(file, correctAnswer)

@app.post("/Q7")
async def speech_to_text_q7(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q4andQ7(file, correctAnswer)

@app.post("/Q7-1")
async def speech_to_text_q7(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q4andQ7(file, correctAnswer)

@app.post("/Q7-2")
async def speech_to_text_q7(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q4andQ7(file, correctAnswer)

@app.post("/Q7-3")
async def speech_to_text_q7(
    file: UploadFile = File(...), 
    correctAnswer: str = Form(...)
):
    return await Q4andQ7(file, correctAnswer)

# 사용시에만 주석제거
# @app.post("/tts")
# async def generate_audio(text: str, filename: str):
#     result = generate_audio(text=text, filename=filename)
#     return result

@app.post("/hq1")
async def hq1(age: str=Form(...), answer: str=Form(...)):
    return  hq1_evaluation(age, answer)

@app.post("/hq2")
async def hq2(answer: str=Form(...)):
    return hq2_evaluation(answer)

@app.post("/hq9")
async def hq9(answer: str=Form(...)):
    return hq9_evaluation(answer)
  
# 데이터 전달
@app.get("/get_explanations")
async def get_explanations(): return explanations

@app.get("/get_scores")
async def get_scores(): return scores
