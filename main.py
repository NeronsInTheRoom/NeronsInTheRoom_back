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
from module.Q1 import q1_evaluation
from module.Q2 import q2_evaluation
from module.Q3 import q3_evaluation
from module.Q3_1 import q3_1_evaluation
from module.Q8 import q8_evaluation
from module.Q8_1 import q8_1_evaluation
from module.Q9 import q9_evaluation
import asyncio
import os
import logging

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
async def speech_to_text(place: str = Form(...), file: UploadFile = File(...)):
    # 파일 확장자 확인
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        logging.error("지원하지 않는 파일 형식입니다.")
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    # 파일 읽기
    contents = await file.read()
    if not contents:
        logging.error("파일 내용이 비어 있습니다.")
        raise HTTPException(status_code=400, detail="파일 내용이 비어 있습니다.")
    
    # 음성 텍스트 변환
    try:
        text = await transcribe_audio(contents)
    except Exception as e:
        logging.error(f"STT 변환 오류: {e}")
        raise HTTPException(status_code=500, detail="STT 변환 중 오류 발생")

    try:
        score = await q3_evaluation(place, text)
    except asyncio.TimeoutError:
        logging.error("Q3 평가 시간 초과")
        raise HTTPException(status_code=500, detail="Q3 평가 시간 초과")
    except Exception as e:
        logging.error(f"Q3 평가 오류: {e}")
        raise HTTPException(status_code=500, detail="Q3 평가 중 오류 발생")
    
    # Q3 평가 결과 반환
    return {
        "score": score,
        "answer": text  
    }

@app.post("/Q3-1")
async def speech_to_text_alternate(place: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    if not contents:
        logging.error("Q3-1: 파일 내용이 비어 있습니다.")
        raise HTTPException(status_code=400, detail="파일 내용이 비어 있습니다.")

    try:
        text = await transcribe_audio(contents)
    except Exception as e:
        logging.error(f"STT 변환 오류(Q3-1): {e}")
        raise HTTPException(status_code=500, detail="STT 변환 중 오류 발생(Q3-1)")

    try:
        score = await q3_1_evaluation(place, text)
    except Exception as e:
        logging.error(f"Q3-1 평가 오류: {e}")
        raise HTTPException(status_code=500, detail="Q3-1 평가 중 오류 발생")
    
    return {
        "score": score,
        "answer": text  
    }
    
@app.post("/Q8")
async def speech_to_text(image_name: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    
    score = await q8_evaluation(image_name, text)
    
    res = {
        "score": score,
        "answer": text  
    }
    
    # 점수가 0일 경우 정답 반환
    if score == 0:
        # 미리 정의된 이미지와 정답 매핑
        image_answers = {
            "clock": "시계",
            "coin": "동전",
            "key": "열쇠",
            "pencil": "연필",
            "stamp": "도장"
        }
        correct_answer = image_answers.get(image_name, "정의되지 않음")
        res["correct_answer"] = correct_answer
        print(f"정답: {res}")
    
    return res

@app.post("/Q8-1")
async def speech_to_text_alternate(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    
    score = await q8_1_evaluation(text)
    
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

# Q8, Q8-1의 이미지 통신 코드
@app.get("/image/{item_name}")
async def get_image(item_name: str):
        # 파일 경로 지정 (예시: "static/img" 폴더 내 이미지)
    image_path = os.path.join("static", "img", f"{item_name}.jpg")
    
    # 이미지 파일이 존재할 경우 반환, 없으면 예외 발생
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}
 
# 데이터 전달
@app.get("/get_explanations")
async def get_explanations(): return explanations

@app.get("/get_scores")
async def get_scores(): return scores
