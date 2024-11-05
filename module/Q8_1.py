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

# Q8-1의 정답 키워드 목록 정의
expected_objects = ["시계", "동전", "열쇠", "연필", "도장"]

# Q8-1 질문 텍스트 가져오기
q8_1_question = next((q["value"] for q in questions if q["key"] == "Q8-1"), None)
if q8_1_question is None:
    raise ValueError("Q8-1 질문을 찾을 수 없습니다.")

async def q8_1_evaluation(answer):
    
    # 예상 객체 목록을 문자열로 정리
    expected_objects_str = ", ".join(expected_objects)
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    - The question provided to the user is: "{q8_1_question}".
    - The expected correct objects that the user might mention include: {expected_objects_str}.
    - The user's response is: "{answer}".
    - Evaluate if "{answer}" includes any of the expected objects listed above. 
    - Return a JSON object with "answer_list" containing the matched objects.
    
    # Output
    {{
        "answer_list": []
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
    
    # 질문 생성 성공
    answers = result["answer_list"]
    num_answer = len(answers)

    # 점수 부여 기준에 따라 점수 계산
    if num_answer >= 5:
        score = 5
    elif num_answer == 4:
        score = 4
    elif num_answer == 3:
        score = 3
    elif num_answer == 2:
        score = 2
    elif num_answer == 1:
        score = 1
    else:
        score = 0
        
    final_result = {
        "score": score,
        "answer": answer,
        "questions": q8_1_question,
        "correctAnswer": expected_objects
    }

    return final_result