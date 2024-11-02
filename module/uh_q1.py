from datetime import datetime
import re

def hq1_evaluation(birth_year, answer):
    
    # 현재 연도 가져오기
    current_year = datetime.now().year
    
    # 출생 연도에서 실제 나이 계산
    birth_year_num = int(re.sub(r'\D', '', birth_year))
    actual_age = current_year - birth_year_num
    
    # 답변에서 숫자만 추출
    answer_num_str = re.sub(r'\D', '', answer)
    if answer_num_str:
        answer_num = int(answer_num_str)
    else:
        print("답변에서 숫자를 찾을 수 없습니다.")
        return {"score": 0}
    
    print(f"출생 연도: {birth_year}, 답변 나이: {answer}")
    print(f"실제 나이: {actual_age}, 답변 나이: {answer_num}")
    
    # 실제 나이 - 답변 나이 = 절대값 구하기
    difference = abs(actual_age - answer_num)
    print(f"절대값: {difference}")
    res_abs = 1 if difference <= 2 else 0
    
    return {"score": res_abs}