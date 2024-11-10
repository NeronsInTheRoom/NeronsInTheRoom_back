from dotenv import load_dotenv
from openai import OpenAI
from data import questions
from datetime import datetime
import os
import json
import re

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

# 생년월일로부터 나이 계산 함수
def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, "%Y%m%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Q1 평가 함수
async def q1_llm_evaluation(birth_date, answer):
    # 실제 나이 계산
    correct_age = calculate_age(birth_date)
    
    # Q1 질문 텍스트 가져오기
    q1_question = next((q["value"] for q in questions if q["key"] == "Q1"), None)
    if q1_question is None:
        raise ValueError("Q1 질문을 찾을 수 없습니다.")
    
    # LLM 호출을 통해 사용자 나이 추출
    system_prompt = f"""
    # Role
    - Extract the user's stated age from their response.

    # Task
    - First, the question received by the user is {q1_question}.
    - Second, the user's answer is "{answer}".
    - Third, extract the age as an integer and output it as JSON.

    # Output
    {{
        "userAge":
    }}
    """
    
    completion = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": answer}
        ],
        temperature=0
    )

    response_content = completion.choices[0].message.content
    
    try:
        result = json.loads(response_content)
        user_age = result["userAge"]
        print(f"LLM 추출된 사용자 나이: {user_age}")
    except json.JSONDecodeError:
        print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
        return None

    if user_age is None:
        raise ValueError("사용자의 답변에서 나이를 파악할 수 없습니다.")

    # 나이 차이 계산
    age_difference = abs(correct_age - user_age)
    print(f"나이 차이: {age_difference}")

    # 나이 차이가 2 이하면 1점, 그렇지 않으면 0점 부여
    score = 1 if age_difference <= 2 else 0

    # JSON 형식으로 결과 반환
    return {
        "score": score,
        "answer": answer,
        "questions": q1_question,
        "correctAnswer": correct_age
    }
