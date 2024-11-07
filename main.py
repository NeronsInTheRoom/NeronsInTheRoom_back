from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from pathlib import Path
from module.stt import transcribe_audio
from data import questions
from data import correctAnswer
from module.Q4andQ7 import Q4AndQ7Score
from module.Q5andQ6 import Q5AndQ6Score
# from module.tts import generate_audio
# from module.tts_Q3_2 import generate_Q3_2
from data import explanations
from data import scores

# 성우현
from module.Q1 import q1_evaluation
from module.Q1_python import q1_p_evaluation
from module.Q2 import q2_evaluation
from module.Q2_python import q2_p_evaluation
from module.Q3 import q3_evaluation
from module.Q3_1 import q3_1_evaluation
from module.Q8 import q8_evaluation
from module.Q8_1 import q8_1_evaluation
from module.Q8_1_jamo import q8_1_jamo_evaluation
from module.Q9 import q9_evaluation
from data import questions
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 사용시에만 주석제거
# @app.post("/tts")
# async def tts(text: str, filename: str):
#     result = await generate_audio(text, filename)
#     return result

# @app.post("/tts_Q3_1")
# async def tts(text: str = Form(...)):
#     result = await generate_Q3_1(text)
#     return result

# @app.post("/tts_Q3_2")
# async def tts(text: str = Form(...)):
#     result = await generate_Q3_2(text)
    
#     # 오디오 파일 경로 설정
#     audio_file_path = Path("static/temp", f"Q3-2.wav")

#     # 오디오 파일이 존재할 경우 반환, 없으면 예외 발생
#     if audio_file_path.exists():
#         return FileResponse(audio_file_path)
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail="오디오 파일을 찾을 수 없습니다."
        # )

# static 폴더 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/start")
async def get_questions():
    try:
        # static/audio 디렉토리의 경로
        audio_dir = Path("static/audio")
        
        # wav 파일 목록 가져오기
        audio_files = []
        if audio_dir.exists():
            audio_files = [
                {
                    "filename": file.name,
                    "url": f"http://localhost:8000/static/audio/{file.name}"  # 전체 URL 제공
                }
                for file in audio_dir.glob("*.wav")
            ]
        
        return {
            "questions": questions, 
            "correctAnswer": correctAnswer,
            "audio_files": audio_files,
            "explanations": explanations,
            "maxScores": scores
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"
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
    # Q3-1.wav 파일 삭제 - 이다정 추가
    temp_file_path = Path("static/temp/Q3-2.wav")
    if temp_file_path.exists():
        temp_file_path.unlink()  # 파일 삭제

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

@app.post("/Q1")
async def speech_to_text(birth_date: str=Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
        
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q1_p_evaluation(birth_date, text)
    
    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result

@app.post("/Q2")
async def speech_to_text(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
            
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q2_p_evaluation(text)
    
    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result

@app.post("/Q3")
async def speech_to_text(place: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q3_evaluation(place, text)
    
    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result

@app.post("/Q3-1")
async def speech_to_text_alternate(place: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q3_1_evaluation(place, text)
    
    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result
    
@app.post("/Q8")
async def speech_to_text(image_name: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q8_evaluation(image_name, text)
    
    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result

@app.post("/Q8-1")
async def speech_to_text_alternate(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q8_1_jamo_evaluation(text)
    
    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result
    
@app.post("/Q9")
async def speech_to_text(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 파일 형식입니다. WAV, MP3, M4A, FLAC 파일만 지원합니다."
        )
    
    contents = await file.read()
    text = await transcribe_audio(contents)
    result = await q9_evaluation(text)

    print(f"result: {json.dumps(result, indent=4, ensure_ascii=False)}")
    
    return result

# Q8의 이미지 통신 코드
@app.get("/image/{item_name}")
async def get_image(item_name: str):
        # 파일 경로 지정 (예시: "static/img" 폴더 내 이미지)
    image_path = os.path.join("static", "img", f"{item_name}.jpg")
    
    # 이미지 파일이 존재할 경우 반환, 없으면 예외 발생
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {"error": "Image not found"}
