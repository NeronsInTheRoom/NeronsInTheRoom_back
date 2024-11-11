from dotenv import load_dotenv
from openai import OpenAI
from data import questions, correctAnswer
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

async def Q4AndQ7Score(text: str):

    # Q4 문제와 정답 가져오기
    q4_question = next((q["value"] for q in questions if q["key"] == "Q4"), None)
    if q4_question is None:
        raise ValueError("Q4 질문을 찾을 수 없습니다.")
    q4_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q4"), None)
    if q4_answer is None:
        raise ValueError("Q4 정답을 찾을 수 없습니다.")

    prompt = f"""
            
    # Role
    You are an expert in evaluating Korean text similarity and scoring responses.
    Your task is to compare user answers with correct answers and score them based on morphological similarity.

    # Important Scoring Rules
    1. Score is based on word presence, NOT order
    2. For scoring process:
    - Each word in user's answer can match ANY word in correct answer
    - Typos that clearly intended the correct answer should be accepted (e.g., '기챠' for '기차', '호낭이' for '호랑이')
    - A word can only be matched once
    3. Final score array MUST follow the correct answer sequence
    4. Return format:
    - Single word: integer (0 or 1)
    - Multiple words: array of integers (0s and 1s) matching CORRECT ANSWER order
    - Example: [0, 1, 1] ✓  [0.0, 1.0, 1.0] ✗

    # Scoring Process
    1. For each word in the CORRECT ANSWER order:
    - Check if this word appears anywhere in user's answer
    - If found (allowing for typos), mark 1
    - If not found, mark 0
    2. Present scores in the CORRECT ANSWER order

    # Examples
    Correct: "기차, 호랑이, 사과"
    User: "사과, 자동차, 호랑이"
    Score: [0, 1, 1] 
    Explanation: 
    - 기차: Not found → 0 (integer)
    - 호랑이: Found → 1 (integer)
    - 사과: Found → 1 (integer)

    Correct: "기차"
    User: "기챠"
    Score: 1 (integer, not 1.0)

    # Context
    - Question: {q4_question} 
    - Correct Answer: {q4_answer}
    - User's Response: {text}

    # Output
    {{
        "score":"",
        "answer": "{text}"
    }}

    CRITICAL NOTE: 
    1. Word order in user's answer does NOT matter for scoring
    2. Each correct word only needs to appear SOMEWHERE in the answer
    3. Final score array MUST match the CORRECT ANSWER sequence
    4. Example: if correct is "기차, 호랑이, 사과" and user writes "사과, 자동차, 호랑이", 
    the score should be [0, 1, 1] because:
    - 기차 is not present (0)
    - 호랑이 is present (1)
    - 사과 is present (1)
    """

    # API 호출
    completion = client.chat.completions.create(
        model=gpt_model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
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