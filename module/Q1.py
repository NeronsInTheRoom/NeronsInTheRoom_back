from datetime import datetime
import re

# 한글 숫자를 정수로 변환하는 함수
def convert_korean_number_to_int(korean_number):
    # 한글 숫자 매핑
    units = {"일": 1, "이": 2, "삼": 3, "사": 4, "오": 5, "육": 6, "칠": 7, "팔": 8, "구": 9, "영": 0}
    tens = {"십": 10, "스물": 20, "서른": 30, "마흔": 40, "쉰": 50, "예순": 60, "일흔": 70, "여든": 80, "아흔": 90}

    result = 0
    current_tens = 0

    # 한글 숫자 문자열을 처리할 수 있도록 수정
    for word in korean_number:
        if word in tens:
            current_tens = tens[word]
        elif word in units:
            result += current_tens + units[word]
            current_tens = 0
        elif word == "십" and current_tens == 0:
            current_tens = 10
        elif word == "십" and current_tens != 0:
            current_tens += 10

    result += current_tens  # 남아있는 십 단위 값 추가

    return result

async def q1_evaluation(birth_date, answer):
    
    # 현재 날짜 가져오기
    current_date = datetime.now()
    
    # 생년월일을 datetime 객체로 변환
    birth_date_str = re.sub(r'\D', '', birth_date)  # 숫자만 추출
    if len(birth_date_str) != 8:
        print("생년월일 형식이 잘못되었습니다. YYYYMMDD 형식이어야 합니다.")
        return {"score": 0}
    
    # 생년월일을 datetime 형식으로 변환
    birth_date_obj = datetime.strptime(birth_date_str, "%Y%m%d")
    
    # 실제 나이 계산
    actual_age = current_date.year - birth_date_obj.year - ((current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day))
    
    # 답변에서 숫자만 추출
    answer = answer.replace(" ", "")  # 공백 제거
    answer = answer.replace("살", "")  # "살" 제거
    answer_num_str = re.sub(r'\D', '', answer)
    
    if answer_num_str:
        answer_num = int(answer_num_str)
    else:
        # 숫자만이 아닌 경우, 한글 숫자를 정수로 변환 시도
        answer_num = convert_korean_number_to_int(answer)
        if answer_num == 0:  # 변환 실패 시
            print("답변에서 숫자를 찾을 수 없습니다.")
            return {"score": 0}
    
    print(f"생년월일: {birth_date}, 답변 나이: {answer}")
    print(f"실제 나이: {actual_age}, 답변 나이: {answer_num}")
    
    # 실제 나이 - 답변 나이 = 절대값 구하기
    difference = abs(actual_age - answer_num)
    print(f"절대값: {difference}")
    res_abs = 1 if difference <= 2 else 0
    
    return {"score": res_abs, "answer": answer_num}