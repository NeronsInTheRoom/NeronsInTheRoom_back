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
    
    max_len = max(len(jamo1), len(jamo2))
    min_len = min(len(jamo1), len(jamo2))
    
    matches = sum(1 for i in range(min_len) if jamo1[i] == jamo2[i])
    similarity = matches / max_len
    
    return similarity

async def q3_1_jamo_evaluation(place, answer):
    print("q3_1_jamo_evaluation 함수 호출")
    # Q3-1 질문 텍스트 가져오기
    q3_1_question = next((q["value"] for q in questions if q["key"] == "Q3-1"), None)
    if q3_1_question is None:
        raise ValueError("Q3-1 질문을 찾을 수 없습니다.")
    
    # 자모 유사도 검사
    similarity = calculate_jamo_similarity(place, answer)
    threshold = 0.7  # 유사도 임계값 설정
    # print(f"유사도 값: {similarity:.3f} (기준 임계값: {threshold})")  # 유사도 값 출력
    
    if similarity >= threshold:
        score = 1
    else:
        # LLM 호출을 통해 추가 확인
        system_prompt = f"""
        # Role
        - You have a scoring system that evaluates the user's answer for a location-based question.

        # Task
        - The actual location of the user is "{place}".
        - The user's answer is "{answer}".
        - Compare if the user's answer is related to or matches the actual location.
        - If related, return a score of 1. If not, return a score of 0.

        # Output
        {{
            "score":,
            "answer":"{answer}",
            "questions":"{q3_1_question}",
            "correctAnswer":"{place}"
        }}
        """
        
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
            result = json.loads(response_content)
            return result
        except json.JSONDecodeError:
            print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
            return None
    
    # JSON 형식으로 반환
    return {
        "score": score,
        "answer": answer,
        "questions": q3_1_question,
        "correctAnswer": place
    }