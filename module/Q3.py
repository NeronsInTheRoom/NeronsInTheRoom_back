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

async def q3_evaluation(place, answer):
    
    # Q3 질문 텍스트 가져오기
    q3_question = next((q["value"] for q in questions if q["key"] == "Q3"), None)
    if q3_question is None:
        raise ValueError("Q3 질문을 찾을 수 없습니다.")
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q3_question}.
    - Second, the user's actual location is {place}.
    - Third, the location where the user answered is {answer}.
    - Fourth, determine if "{answer}" describes an activity, purpose, or function that is typically associated with the location "{place}".
    - Fifth, if "{answer}" is related to or within "{place}", assign a score of 2 in JSON format. If not, assign a score of 0.
    
    # Score
    - The user's score is placed in the "score" type in the JSON output.
    
    # Output
    {{
        "score":"",
        "answer":"{answer}",
        "questions":"{q3_question}",
        "correctAnswer":"{place}"
        
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
        return result
    except json.JSONDecodeError:
        print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
        return None