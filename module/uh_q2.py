from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import datetime
import re

def hq2_evaluation(answer):
    
    # NER 모델과 토크나이저 로드
    model_name = "KoichiYasuoka/roberta-large-korean-upos"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    
    # 오늘 년, 월, 일 가져오기
    today = datetime.datetime.now()
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
    # print(f"{current_year}년 {current_month}월 {current_day}일, {current_weekday}")
    
    # NER 모델로 날짜 정보 추출
    entities = ner(answer)
    
    year, month, day, weekday = None, None, None, None
    for entity in entities:
        if "년" in entity["word"]:
            match = re.search(r'\d+', entity["word"])
            if match:
                year = int(match.group())
        elif "월" in entity["word"]:
            match = re.search(r'\d+', entity["word"])
            if match:
                month = int(match.group())
        elif re.search(r'\d+일', entity["word"]):
            match = re.search(r'\d+', entity["word"])
            if match:
                day = int(match.group())
        elif "요일" in entity["word"]:
            weekday = entity["word"]
                
    # 점수 계산
    score = 0
    if year == current_year:
        score += 1
    if month == current_month:
        score += 1
    if day == current_day:
        score += 1
    if weekday == current_weekday:
        score += 1
    
    return {"score": score}