from dotenv import load_dotenv
from openai import OpenAI
from data import questions
from datetime import datetime
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

# 오늘 날짜 정보 가져오기
today = datetime.now()
current_year = today.year
current_month = today.month
current_day = today.day

# 영문 요일을 한글로 매핑
weekday_korean = {
    "Monday": "월요일",
    "Tuesday": "화요일",
    "Wednesday": "수요일",
    "Thursday": "목요일",
    "Friday": "금요일",
    "Saturday": "토요일",
    "Sunday": "일요일"
}

# 오늘 요일 가져오기
current_weekday = weekday_korean[today.strftime("%A")]

# 오늘 날짜
today = f"{current_year}년 {current_month}월 {current_day}일 {current_weekday}"

async def q2_evaluation(answer):
    
    # Q2 질문 텍스트 가져오기
    q2_question = next((q["value"] for q in questions if q["key"] == "Q2"), None)
    if q2_question is None:
        raise ValueError("Q2 질문을 찾을 수 없습니다.")
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q2_question}.
    - Second, today is {today}.
    - Third, the date the user answered is {answer}.
    - Fourth, compare today's date with the date the user answered.
    - Fifth, 1 point is assigned for each correct answer among year, month, day, and day of the week.
    
    # Output
    {{
        "score":"",
        "answer":"",
        "questions":"",
        "correctAnswer":""
        
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
    
    try:
        # 결과를 JSON 형식으로 로드하여 반환
        result = json.loads(response_content)
        return result
    except json.JSONDecodeError:
        print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
        return None