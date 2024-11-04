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

async def q8_1_evaluation(answer):
    
    system_prompt = f"""
    
    # Role
    - You are a language model that evaluates Korean object names mentioned in a response against a predefined list of objects.

    # Task
    - First, if you have a single string of Korean object names written together without spaces, separate each word.
    - Second, if words with the same meaning, such as "clock", "coin", "key", "pencil", and "stamp", are listed in an array.
    - Lists separated words in JSON array format.
    
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

    return ({"score": score})