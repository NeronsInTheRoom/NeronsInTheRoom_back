from data import questions, correctAnswer
from datetime import datetime
import re

# 생년월일로부터 나이 계산 함수
def calculate_age(birth_date_str):
    birth_date = datetime.strptime(birth_date_str, "%Y%m%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# correctAnswer 리스트의 Q1 업데이트 함수
def update_correct_answer_with_age(birth_date_str):
    correct_age = calculate_age(birth_date_str)  # 실제 나이 계산
    for answer in correctAnswer:
        if answer["key"] == "Q1":
            answer["value"] = str(correct_age)  # 나이를 문자열로 변환하여 저장
            break

# 사용자의 나이 응답 파싱 함수
def parse_age(answer):
    # 숫자+살 형태의 답변 처리
    num_match = re.search(r'(\d+)', answer)
    if num_match:
        year_or_age = int(num_match.group(1))
        
        # 만약 1900년대, 2000년대 생년을 짧게 표현한 경우
        if "년" in answer or "생" in answer:
            today = datetime.today().year
            # 100 이하의 숫자면 이를 연도로 간주하여 현재 연도로부터 나이를 계산
            if year_or_age < 100:
                birth_year = 1900 + year_or_age if year_or_age > 21 else 2000 + year_or_age
                calculated_age = today - birth_year
                return calculated_age, f"{calculated_age}살"
            # 정확한 연도로 제공된 경우 (예: 1996년, 2001년)
            elif year_or_age >= 1900:
                calculated_age = today - year_or_age
                return calculated_age, f"{calculated_age}살"
        else:
            # '나이+살' 형태로 숫자를 반환
            return year_or_age, f"{year_or_age}살"
    
    # 한글로 된 나이 (예: 스물아홉살)를 숫자로 변환
    korean_numbers = {
        "하나": 1, "둘": 2, "셋": 3, "넷": 4, "다섯": 5, "여섯": 6, "일곱": 7, "여덟": 8, "아홉": 9,
        "열": 10, "스물": 20, "서른": 30, "마흔": 40, "쉰": 50, "예순": 60, "일흔": 70, "여든": 80, "아흔": 90
    }
    age = 0
    for word in korean_numbers:
        if word in answer:
            age += korean_numbers[word]
    
    return (age if age > 0 else None), (f"{age}살" if age > 0 else None)  # 숫자와 '숫자살' 형태를 함께 반환

# Q1 평가 함수
async def q1_p_evaluation(birth_date, answer):
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
    
    # 실제 나이와 입력 나이의 차이 계산
    age_difference = abs(correct_age - user_age)
    score = 1 if age_difference <= 2 else 0  # 차이가 2 이하면 1점, 그렇지 않으면 0점

    # JSON 출력 템플릿
    result = {
        "score": str(score),
        "answer": numeric_answer,
        "questions": q1_question,
        "correctAnswer": str(correct_age)
    }
    
    return result