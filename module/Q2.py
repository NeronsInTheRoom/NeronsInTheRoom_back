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

# 사용자 답변에서 년, 월, 일, 요일 추출하기
def parse_date_answer(answer):
    # 연도, 월, 일, 요일에 해당하는 패턴을 정규식으로 추출
    year_match = re.search(r'(\d{4})년', answer)
    month_match = re.search(r'(\d{1,2})월', answer)
    day_match = re.search(r'(\d{1,2})일', answer)
    weekday_match = re.search(r'(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', answer)
    
    # 매칭된 값을 변수에 저장, 매칭되지 않을 경우 None으로 설정
    year = int(year_match.group(1)) if year_match else None
    month = int(month_match.group(1)) if month_match else None
    day = int(day_match.group(1)) if day_match else None
    weekday = weekday_match.group(1) if weekday_match else None
    
    print(f"연도: {year}, 월: {month}, 일: {day}, 요일: {weekday}")
    
    return year, month, day, weekday

async def q2_evaluation(answer):
    # 사용자 답변에서 년, 월, 일, 요일 추출하기
    year, month, day, weekday = parse_date_answer(answer)
    
    # Q2 질문 텍스트 가져오기
    q2_question = next((q["value"] for q in questions if q["key"] == "Q2"), None)
    if q2_question is None:
        raise ValueError("Q2 질문을 찾을 수 없습니다.")
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q2_question}.
    - Second, year comparison
        - First, today is {current_year}.
        - Second, the user answered today is {year}.
        - Third, if {current_year} and {year} match, 1 point is assigned.
    - Third, month comparison
        - First, today is {current_month}.
        - Second, the user answered today is {month}.
        - Third, if {current_month} and {month} match, 1 point is assigned.
    - Fourth, day comparison
        - First, today is {current_day}.
        - Second, today, as the user answered, is {day}.
        - Third, if {current_day} and {day} match, 1 point is assigned.
    - Fifth, compare days of the week
        - First, today is {current_weekday}.
        - Second, today as the user answered is {weekday}.
        - Third, if {current_weekday} and {weekday} match, 1 point is assigned.
    
    # Output
    {{
        "score":,
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