from jamo import h2j, j2hcj
from data import questions
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

# Q8-1의 정답 키워드 목록 정의
expected_objects = ["시계", "동전", "열쇠", "연필", "도장"]

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

# q8_1_jamo_evaluation 수정
async def question8_1(answer):
    
    # Q8-1 질문 텍스트 가져오기
    q8_1_question = next((q["value"] for q in questions if q["key"] == "Q8-1"), None)
    if q8_1_question is None:
        raise ValueError("Q8-1 질문을 찾을 수 없습니다.")
    
    # 예상 객체 목록을 문자열로 정리
    expected_objects_str = ", ".join(expected_objects)
    
    system_prompt = f"""
    
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    - The question provided to the user is: "{q8_1_question}".
    - The expected correct objects that the user might mention include: {expected_objects_str}.
    - The user's response is: "{answer}".
    - Evaluate if "{answer}" includes any of the expected objects listed above. 
    - Return a JSON object with "answer_list" containing the matched objects.
    
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
    
    # 결과를 JSON 형식으로 로드하여 반환
    result = json.loads(response_content)
    print(f"LLM 결과 확인: {result}")

    if result is None:
        print("result None입니다. result 값을 확인하세요.")
        return {"error": "result 값이 None입니다."}  # 에러 핸들링 추가
    
    # 정답 키워드와 각각의 임계값 목록
    expected_objects_with_thresholds = [
        ("시계", 0.8),
        ("동전", 0.8),
        ("열쇠", 0.8),
        ("연필", 0.8),
        ("도장", 0.8)
    ]
    
    # 사용자 답변 자모 분해 및 비교
    matched_objects = []

    # 점수 부여 및 매칭 수정
    for ans_word in result.get("answer_list", []):
        for correct_word, threshold in expected_objects_with_thresholds:
            similarity = calculate_jamo_similarity(ans_word, correct_word)
            print(f"Comparing '{ans_word}' with '{correct_word}': similarity = {similarity:.3f}, threshold = {threshold}")
            if similarity >= threshold:  # 임계값을 만족하는 경우
                matched_objects.append(correct_word)
                break

    # 중복 제거
    matched_objects = list(set(matched_objects))
    print(f"Matched objects: {matched_objects}")
    num_answer = len(matched_objects)

    # 점수 부여
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

    final_result = {
        "score": score,
        "answer": answer,
        "questions": q8_1_question,
        "correctAnswer": [word for word, _ in expected_objects_with_thresholds]
    }
    
    return final_result