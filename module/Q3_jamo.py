from dotenv import load_dotenv
from openai import OpenAI
from data import questions
from jamo import h2j, j2hcj
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

# 자모 기반 한글 분해 함수
def decompose_hangul(word):
    """한글 단어를 자모 단위로 분해"""
    return list(j2hcj(h2j(word)))

# 자모 기반 유사도 계산 함수
def calculate_jamo_similarity(word1, word2):
    """두 단어 간의 자모 유사도 계산"""
    jamo1 = decompose_hangul(word1)
    jamo2 = decompose_hangul(word2)
    
    print(f"Decomposed '{word1}': {jamo1}")
    print(f"Decomposed '{word2}': {jamo2}")
    
    max_len = max(len(jamo1), len(jamo2))
    min_len = min(len(jamo1), len(jamo2))
    
    matches = sum(1 for i in range(min_len) if jamo1[i] == jamo2[i])
    print(f"Matches: {matches}, Max length: {max_len}")
    
    similarity = matches / max_len
    return similarity

async def q3_jamo_evaluation(place, answer):
    
    # Q3 질문 텍스트 가져오기
    q3_question = next((q["value"] for q in questions if q["key"] == "Q3"), None)
    if q3_question is None:
        raise ValueError("Q3 질문을 찾을 수 없습니다.")
    
    # 초기 점수를 0으로 설정
    score = 0
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q3_question}.
    - Second, the user's actual location is {place}.
    - Third, the location where the user answered is {answer}.
    - Fourth, determine if "{answer}" describes an activity, purpose, or function that is typically associated with the location "{place}".
    - Fifth, if "{answer}" is related to or within a "{place}", only that place will be assigned the user's answer in JSON format.
    
    # Score
    - The user's score is placed in the "score" type in the JSON output.
    
    # Output
    {{
        "answer":
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
    print(f"LLM 결과 확인: {result}")
    
    if result is None:
        print("result None입니다. result 값을 확인하세요.")
        return {"error": "result 값이 None입니다."}  # 에러 핸들링 추가
    
    # 자모 유사도 검사
    threshold = 0.7  # 유사도 임계값 설정
    term = result.get("answer")
    
        # term이 문자열이 아닌 경우 문자열로 변환
    if term and isinstance(term, str):
        similarity = calculate_jamo_similarity(place, term)
        print(f"'{place}'와 '{term}' 비교: 유사도 = {similarity:.3f}, 임계값 = {threshold}")
        if similarity >= threshold:
            score = 1
    else:
        print(f"올바른 문자열이 아닙니다: {term}")

    # JSON 형식으로 결과 반환
    return {
        "score": score,
        "answer": answer,
        "questions": q3_question,
        "correctAnswer": place
    }