from datetime import datetime
from data import questions
import re
from jamo import h2j, j2hcj

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

# 한글 단어를 자모(음운 단위)로 분해하는 함수
def decompose_hangul(word):
    """한글 단어를 자모 단위로 분해"""
    return list(j2hcj(h2j(word)))

# 자모 기반 유사도 계산 함수
def calculate_jamo_similarity(word1, word2):
    """두 단어 간의 자모 유사도 계산"""
    jamo1 = decompose_hangul(word1)
    jamo2 = decompose_hangul(word2)
    
    max_len = max(len(jamo1), len(jamo2))
    min_len = min(len(jamo1), len(jamo2))
    
    matches = sum(1 for i in range(min_len) if jamo1[i] == jamo2[i])
    similarity = matches / max_len
    
    return similarity

# 사용자 답변에서 년, 월, 일, 요일 추출하기
def parse_date_answer(answer):
    year_match = re.search(r'(\d{4})년', answer)
    month_match = re.search(r'(\d{1,2})월', answer)
    day_match = re.search(r'(\d{1,2})일', answer)
    weekday_match = re.search(r'(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', answer)
    
    year = int(year_match.group(1)) if year_match else None
    month = int(month_match.group(1)) if month_match else None
    day = int(day_match.group(1)) if day_match else None
    weekday = weekday_match.group(1) if weekday_match else None
    
    return year, month, day, weekday

# 날짜를 비교하고 점수를 계산하는 함수
async def q2_jamo_evaluation(answer):
    # 사용자가 입력한 날짜 정보 추출
    user_year, user_month, user_day, user_weekday = parse_date_answer(answer)
    
    # 각 항목을 비교하고 점수 계산
    score = 0
    correct_answer = f"{current_year}년 {current_month}월 {current_day}일 {current_weekday}"
    
    if user_year == current_year:
        score += 1
    if user_month == current_month:
        score += 1
    if user_day == current_day:
        score += 1

    # 요일 자모 비교
    if user_weekday:
        similarity = calculate_jamo_similarity(current_weekday, user_weekday)
        print(f"'{current_weekday}'와 '{user_weekday}' 비교: 유사도 = {similarity:.3f}")
        if similarity >= 0.6:  # 유사도 임계값 설정
            score += 1
    
    # Q2 질문 텍스트 가져오기
    q2_question = next((q["value"] for q in questions if q["key"] == "Q2"), None)
    if q2_question is None:
        raise ValueError("Q2 질문을 찾을 수 없습니다.")

    # 결과 출력
    result = {
        "score": score,
        "answer": answer,
        "questions": q2_question,
        "correctAnswer": correct_answer
    }
    
    return result
