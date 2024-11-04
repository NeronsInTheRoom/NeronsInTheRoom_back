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

async def q3_1_evaluation(place, answer):
    
    system_prompt = f"""
    
    # Role
    - You are an expert location comparer.

    # Task
    - First, the user's actual location: "{place}".
    - Second, the location answered by the user in response to the question "지금 있는 곳이 병원인가요? 집인가요?": "{answer}".
    - Third, evaluate how well "{answer}" matches the user's actual location "{place}".
    - Focus on whether "{answer}" clearly identifies or matches the specific place represented by "{place}" rather than describing possible activities or functions.
    - For example, if "{place}" is "병원", acceptable answers would include "병원" or similar direct identifiers. If "{place}" is "집", acceptable answers might be "집" or equivalent terms.
    - Fourth, if "{answer}" matches "{place}", assign a score of 1 in JSON format. If it does not match, assign a score of 0.

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
        return result["score"]
    except json.JSONDecodeError:
        print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
        return None