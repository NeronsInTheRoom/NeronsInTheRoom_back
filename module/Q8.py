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

# 미리 정의된 객체 리스트
object_list = {
    "item1": "시계",
    "item2": "열쇠",
    "item3": "도장",
    "item4": "연필",
    "item5": "동전"
}

def q8_evaluation(answer):
    
    system_prompt = f"""
    
    # Role
    You are a language model that identifies individual Korean words within a continuous string of text.

    # Task
    Given a single string of Korean object names written together without spaces, separate each word and list them separated by commas.
    
    # Policy
    - Responses must be in Korean only, without any Chinese characters or mixed languages.
    - Provide the list of identified vegetables in the following JSON array format
    
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
    
    # 점수 계산
    score = sum(1 for answer in result["answer_list"] if answer in object_list.values())
   
    return {"score": score}