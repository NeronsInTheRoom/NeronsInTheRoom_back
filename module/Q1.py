from dotenv import load_dotenv
from openai import OpenAI
from data import questions, correctAnswer
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

# correctAnswer 리스트의 Q1 업데이트 함수
def update_correct_answer_with_age(birth_date_str):
    correct_age = calculate_age(birth_date_str)  # 실제 나이 계산
    # print(f"Calculated age: {correct_age}")  # 디버깅 메시지 추가
    
    for answer in correctAnswer:
        if answer["key"] == "Q1":
            answer["value"] = str(correct_age)  # 나이를 문자열로 변환하여 저장
            # print(f"Updated correctAnswer: {correctAnswer}")  # 업데이트 후 확인
            break

# 사용자의 나이 응답 파싱 함수
def parse_age(answer):
    # 숫자+살 형태의 답변 처리
    num_match = re.search(r'(\d+)', answer)
    if num_match:
        return int(num_match.group(1)), f"{num_match.group(1)}살"  # 숫자와 '숫자살' 형태를 함께 반환
    
    # 한글로 된 나이 (예: 스물 한 살)를 숫자로 변환
    korean_numbers = {
        "하나": 1, "둘": 2, "셋": 3, "넷": 4, "다섯": 5, "여섯": 6, "일곱": 7, "여덟": 8, "아홉": 9,
        "열": 10, "열한": 11, "열두": 12, "열세": 13, "열네": 14, "열다섯": 15, "열여섯": 16, "열일곱": 17, "열여덟": 18, "열아홉": 19,
        "스물": 20, "스물한": 21, "스물두": 22, "스물세": 23, "스물네": 24, "스물다섯": 25, "스물여섯": 26, "스물일곱": 27, "스물여덟": 28, "스물아홉": 29,
        "서른": 30, "서른한": 31, "서른두": 32, "서른세": 33, "서른네": 34, "서른다섯": 35, "서른여섯": 36, "서른일곱": 37, "서른여덟": 38, "서른아홉": 39,
        "마흔": 40, "마흔한": 41, "마흔두": 42, "마흔세": 43, "마흔네": 44, "마흔다섯": 45, "마흔여섯": 46, "마흔일곱": 47, "마흔여덟": 48, "마흔아홉": 49,
        "쉰": 50, "쉰한": 51, "쉰두": 52, "쉰세": 53, "쉰네": 54, "쉰다섯": 55, "쉰여섯": 56, "쉰일곱": 57, "쉰여덟": 58, "쉰아홉": 59,
        "예순": 60, "예순한": 61, "예순두": 62, "예순세": 63, "예순네": 64, "예순다섯": 65, "예순여섯": 66, "예순일곱": 67, "예순여덟": 68, "예순아홉": 69,
        "일흔": 70, "일흔한": 71, "일흔두": 72, "일흔세": 73, "일흔네": 74, "일흔다섯": 75, "일흔여섯": 76, "일흔일곱": 77, "일흔여덟": 78, "일흔아홉": 79,
        "여든": 80, "여든한": 81, "여든두": 82, "여든세": 83, "여든네": 84, "여든다섯": 85, "여든여섯": 86, "여든일곱": 87, "여든여덟": 88, "여든아홉": 89,
        "아흔": 90, "아흔한": 91, "아흔두": 92, "아흔세": 93, "아흔네": 94, "아흔다섯": 95, "아흔여섯": 96, "아흔일곱": 97, "아흔여덟": 98, "아흔아홉": 99
    }
    age = 0
    for word in korean_numbers:
        if word in answer:
            age += korean_numbers[word]
    
    return (age if age > 0 else None), (f"{age}살" if age > 0 else None)  # 숫자와 '숫자살' 형태를 함께 반환

# Q1 평가 함수
async def q1_evaluation(birth_date, answer):
    # 실제 나이 계산
    correct_age = calculate_age(birth_date)
    
    # Q1 질문 텍스트 가져오기
    q1_question = next((q["value"] for q in questions if q["key"] == "Q1"), None)
    if q1_question is None:
        raise ValueError("Q1 질문을 찾을 수 없습니다.")
    
    # 사용자의 나이 응답 파싱
    user_age, numeric_answer = parse_age(answer)  # numeric_answer는 "숫자살" 형태의 문자열
    if user_age is None:
        raise ValueError("사용자의 답변에서 나이를 파악할 수 없습니다.")
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q1_question}.
    - Second, the user's actual age is {correct_age}.
    - Third, the age answered by the user is {user_age}.
    - Fourth, compare the user's actual age with the age answered by the user.
    - Fifth, the margin of error for age can be up to 2 years.
    - Sixth, 1 point for a correct answer and 0 points for an incorrect answer are assigned to the "score" type of the JSON output.
    
    # Output
    {{
        "score":"",
        "answer":"{numeric_answer}",
        "questions":"{q1_question}",
        "correctAnswer":"{correct_age}"
        
    }}
    """
    
    # API 호출
    completion = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": numeric_answer}  # 한글 대신 숫자 변환 형태 사용
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