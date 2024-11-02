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

def hq3_gpt_evaluation(location, answer):
    
    system_prompt = f"""
    
    # Role
    - You are an expert location comparer.

    # Task
    - First, the user's actual location: "{location}".
    - Second, the location answered by the user: "{answer}".
    - Third, determine if "{answer}" is a plausible description or location within "{location}" (e.g., "치료받는 곳" is within "병원").
    - Fourth, if "{answer}" is related to or within "{location}", assign a score of 2 in JSON format. If not, assign a score of 0.
    
    # Output
    {{
        "score":
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