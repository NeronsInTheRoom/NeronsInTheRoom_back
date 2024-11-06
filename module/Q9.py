from dotenv import load_dotenv
from openai import OpenAI
from data import questions
import os
import json

load_dotenv()

# API_KEY 가져오기
api_key = os.getenv("API_KEY")
if api_key is None:
    raise ValueError("API_KEY가 없습니다.")

# GPT 모델 가져오기
gpt_model = os.getenv("GPT")
if gpt_model is None:
    raise ValueError("GPT_Model이 없습니다.")

# OpenAI 클라이언트 초기화 및 API 키 등록
client = OpenAI(api_key=api_key)

# Q9의 정답 키워드 예시 목록 정의
expected_objects = [
    "배추", "무", "상추", "시금치", "깻잎", 
    "대파", "부추", "열무", "고추", "오이", 
    "호박", "가지", "콩나물", "마늘"
]

async def q9_evaluation(answer):
    
    # Q9 질문 텍스트 가져오기
    q9_question = next((q["value"] for q in questions if q["key"] == "Q9"), None)
    if q9_question is None:
        raise ValueError("Q9 질문을 찾을 수 없습니다.")
        
    system_prompt = f"""
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q9_question}.
    - Second, the location where the user answered is {answer}.
    - Third, identify the presence of “vegetables” in the user’s answer.
    - Fourth, if there are duplicate vegetables, they are excluded.
    - Fifth, if there are any "vegetables" identified, it returns a JSON object containing a "vegetable_list".
    
    # Output
    {{
        "vegetable_list": []
    }}
    """
    
    # API 호출
    completion = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": answer}
        ],
        temperature=0
    )

    response_content = completion.choices[0].message.content
    result = json.loads(response_content)

    # 질문 생성 성공
    vegetable_list = result["vegetable_list"]
    # 중복 제거 후 리스트
    print(f"중복 제거 후 리스트: {vegetable_list}")
    num_vegetables = len(vegetable_list)

    # 점수 부여 기준에 따라 점수 계산
    if num_vegetables >= 10:
        score = 5
    elif num_vegetables == 9:
        score = 4
    elif num_vegetables == 8:
        score = 3
    elif num_vegetables == 7:
        score = 2
    elif num_vegetables == 6:
        score = 1
    else:
        score = 0

    final_result = {
        "score": score,
        "answer": answer,
        "questions": q9_question,
        "correctAnswer": expected_objects
    }
    
    return final_result