from dotenv import load_dotenv
from openai import OpenAI
from data import questions
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

# 이미지 이름에 따른 정답 키워드 목록 정의
image_keywords = {
    "clock": ["시계", "벽시계"],
    "coin": ["동전", "돈"],
    "key": ["열쇠", "키"],
    "pencil": ["연필", "펜"],
    "stamp": ["도장"]
}

# 이미지 이름을 한글로 매핑하는 딕셔너리
image_name_korean = {
    "clock": "시계",
    "coin": "동전",
    "key": "열쇠",
    "pencil": "연필",
    "stamp": "도장"
}

async def question8(image_name, answer):
    
    # Q8 질문 텍스트 가져오기
    q8_question = next((q["value"] for q in questions if q["key"] == "Q8"), None)
    if q8_question is None:
        raise ValueError("Q8 질문을 찾을 수 없습니다.")
    
    # 이미지 이름에 해당하는 정답 키워드 목록 가져오기
    correct_keywords = image_keywords.get(image_name, [])
    keywords_str = ", ".join(correct_keywords)
    
    # 이미지 이름을 한글로 변환
    correct_answer_korean = image_name_korean.get(image_name, image_name)
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.
    
    # Task
    - The user is viewing an image of a "{image_name}".
    - Expected correct answers for this image include the following keywords: {keywords_str}.
    - The user's answer is "{answer}".
    - Evaluate whether "{answer}" matches any of the correct keywords associated with "{image_name}".
    - If "{answer}" is similar to one of the keywords, give "y" in JSON format. If no match is found, "n" is given.
    
    # Output
    {{
        "isTrue":,
        "answer":"{answer}",
        "questions":"{q8_question}",
        "correctAnswer":"{correct_answer_korean}"
        
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
    except json.JSONDecodeError:
        print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
        return None
    
    return result