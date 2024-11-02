from datetime import datetime
import re

def q1_evaluation(birth_date, answer):
    
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
    answer_num_str = re.sub(r'\D', '', answer)
    if answer_num_str:
        answer_num = int(answer_num_str)
    else:
        print("답변에서 숫자를 찾을 수 없습니다.")
        return {"score": 0}
    
    print(f"생년월일: {birth_date}, 답변 나이: {answer}")
    print(f"실제 나이: {actual_age}, 답변 나이: {answer_num}")
    
    # 실제 나이 - 답변 나이 = 절대값 구하기
    difference = abs(actual_age - answer_num)
    print(f"절대값: {difference}")
    res_abs = 1 if difference <= 2 else 0
    
    return {"score": res_abs}