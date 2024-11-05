from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import datetime
import re

async def q2_evaluation(answer):
    
    # NER 모델과 토크나이저 로드
    model_name = "KoichiYasuoka/roberta-large-korean-upos"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    
    # 오늘 날짜 정보 가져오기
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
    
    # NER 모델로 날짜 정보 추출
    entities = ner(answer)
    
    # 날짜 정보 초기화
    year, month, day, weekday = None, None, None, None

    # 엔티티 반복 처리
    for entity in entities:
        entity_text = entity["word"]
                
        # 연도 추출
        if "년" in entity_text:
            match = re.search(r'\d+', entity_text)
            if match:
                year = int(match.group())
                
        # 월 추출
        elif "월" in entity_text and "요일" not in entity_text:  # 요일이 아닌 월 추출
            match = re.search(r'\d+', entity_text)
            if match:
                month = int(match.group())
                
        # 일 추출
        elif "일" in entity_text and "요일" not in entity_text:
            match = re.search(r'\d+', entity_text)
            if match:
                day = int(match.group())
        
        # 요일 추출
        elif "요일" in entity_text:
            weekday_match = re.search(r'(월요일|화요일|수요일|목요일|금요일|토요일|일요일)', entity_text)
            if weekday_match:
                weekday = weekday_match.group()
                
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