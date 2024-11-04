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

async def q8_evaluation(image_name, answer):
    
    system_prompt = f"""
    
    # Role
    - You are an expert in identifying objects and determining if a given description accurately matches the object.
    
    # Task
    - First, here is the image object {image_name} that the user asked a question about.
    - Second, the following is an answer {answer} based on the user's question.
    - Third, compare {image_name} and {answer} to evaluate whether they match.
    - Fourth, if “{answer}” is similar to “{image_name}”, 1 point is given in JSON format. If there is no match, 0 points are given.
    
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
    
    return result['score']