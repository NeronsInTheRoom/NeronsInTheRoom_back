from dotenv import load_dotenv
from openai import OpenAI
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

def q9_evaluation(answer):
        
    system_prompt = f"""
    # Role
    - You are a professional vegetable identifier who identifies vegetables.

    # Task
    - Given a single string of vegetable names without spaces, separate and identify each vegetable name.
    - The identified vegetables are actually Check if the vegetables are present.
    
    # Policy
    - Responses must be in Korean only, without any Chinese characters or mixed languages.
    - Provide the list of identified vegetables in the following JSON array format
    
    # Output Example
    {{
        "vegetable_list": ["채소1", "채소2", "채소3"...]
    }}
    
    # Output
    {{
        "vegetable_list": []
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
    result = json.loads(response_content)

    # 질문 생성 성공
    vegetable_list = result["vegetable_list"]
    num_vegetables = len(vegetable_list)

    # 점수 부여 기준에 따라 점수 계산
    if num_vegetables >= 10:
        score = 5
    elif num_vegetables == 9:
        score = 4
    elif num_vegetables == 8:
        score = 3
    elif num_vegetables == 7:
        score = 2
    elif num_vegetables == 6:
        score = 1
    else:
        score = 0

    return ({"score": score})