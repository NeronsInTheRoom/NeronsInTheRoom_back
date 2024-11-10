from dotenv import load_dotenv
from openai import OpenAI
from data import questions
from jamo import h2j, j2hcj
import os
import json
import random

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

# Q9의 정답 키워드 예시 목록 정의
expected_objects = [
    "배추", "무", "상추", "시금치", "깻잎", 
    "대파", "부추", "열무", "고추", "오이", 
    "호박", "가지", "콩나물", "마늘", "파프리카", 
    "당근", "브로콜리", "양배추", "케일", "아스파라거스", 
    "토마토", "셀러리", "고구마", "감자", "비트", 
    "양파", "피망", "파슬리", "완두콩", "청경채", 
    "근대", "루꼴라", "브뤼셀 스프라우트", "아티초크", "방울토마토",
    "레디쉬", "애호박", "순무", "옥수수", "고사리", 
    "우엉", "연근", "새송이버섯", "표고버섯", "느타리버섯", 
    "팽이버섯", "치커리", "양상추", "비타민채", "로메인", 
    "고추냉이", "냉이", "쑥갓", "청피망", "빨강피망", 
    "샐러리악", "에다마메", "열대과일", "크레송", "애플민트",
    "차이브", "차이니즈 브로콜리", "청양고추", "로즈마리", "타임",
    "파인애플 민트", "코리앤더", "민트", "스위스 차드", "바질",
    "라디키오", "에스카롤", "라임콩", "차요테", "기장", 
    "콩잎", "방울양배추", "로켓샐러드", "피클", "발레리안 루트",
    "무청", "깻잎순", "달래", "미나리", "도라지", 
    "더덕", "인삼", "홍삼", "삽주", "소엽", 
    "쑥", "부들레기", "방풍", "칠리", "파",
    "레몬그라스", "올리브", "토란", "죽순", "무말랭이",
    "겨자잎", "순채", "갓", "마룻잎", "노각", 
    "나물콩", "머위", "시래기", "톳", "파드득나물",
    "고들빼기", "고춧잎", "곰취", "다래순", "달맞이꽃잎", 
    "두릅", "명이나물", "방아", "비름나물", "산딸기잎",
    "삼채", "쇠비름", "야생마늘", "여주", "오갈피나무 잎", 
    "옻나무 잎", "작두콩", "칡잎", "패랭이꽃잎", "함박꽃잎",
    "호장근", "호박순", "호미줄기", "효소나물", "원추리", 
    "잔대", "잔디나물", "전호나물", "젖새", "초석잠",
    "참나물", "참취", "큰도꼬마리", "털도라지", "파수세미",
    "한련초", "환삼덩굴", "해초", "말굽버섯", "지렁이풀",
    "보리수잎", "서양고추냉이", "산호상추", "새발나물", "알팔파",
    "바위취", "흑미나리", "황기", "회향잎", "다시마잎",
    "카레잎", "카사바 잎", "차나무잎", "피망잎", "페이퍼리프",
    "사탕수수잎", "쑥부쟁이", "칠리페퍼", "트럼펫버섯", "감자잎",
    "벚꽃잎", "제피", "부추꽃", "산머루잎", "구절초",
    "산딸기순", "줄기콩", "황금잔디", "톨파", "콩나물 뿌리",
    "고사리줄기", "명아주", "깻잎말이", "상추꼬리", "하수오",
    "수영", "새깻잎", "참깨잎", "도깨비바늘", "청나래새싹",
    "서리태잎", "보리새싹", "검은콩나물", "묵나물", "피마자잎"
]

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

async def question9(answer):
    # Q9 질문 텍스트 가져오기
    q9_question = next((q["value"] for q in questions if q["key"] == "Q9"), None)
    if q9_question is None:
        raise ValueError("Q9 질문을 찾을 수 없습니다.")
        
    system_prompt = f"""
    # Role
    - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

    # Task
    - First, the question received by the user is {q9_question}.
    - Second, the location where the user answered is {answer}.
    - Third, identify the presence of “vegetables” in the user’s answer.
    - Fourth, if there are duplicate vegetables, they are excluded.
    - Fifth, if there are any "vegetables" identified, it returns a JSON object containing a "vegetable_list".
    
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

    if result is None:
        print("result None입니다. result 값을 확인하세요.")
        return {"error": "result 값이 None입니다."}  # 에러 핸들링 추가

    # LLM에서 추출한 결과
    vegetable_list = result.get("vegetable_list", [])
    
    # 자모 유사도 체크
    matched_objects = []
    threshold = 0.7  # 유사도 임계값 설정

    for ans_word in vegetable_list:
        for correct_word in expected_objects:
            similarity = calculate_jamo_similarity(ans_word, correct_word)
            print(f"Comparing '{ans_word}' with '{correct_word}': similarity = {similarity:.3f}, threshold = {threshold}")
            if similarity >= threshold:
                matched_objects.append(correct_word)
                break

    # 중복 제거 후 리스트
    matched_objects = list(set(matched_objects))
    print(f"중복 제거 후 리스트: {matched_objects}")

    # 랜덤으로 10개의 채소 선택
    if len(matched_objects) > 10:
        matched_objects = random.sample(matched_objects, 10)

    num_vegetables = len(matched_objects)

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

    final_result = {
        "score": score,
        "answer": answer,
        "questions": q9_question,
        "correctAnswer": expected_objects
    }
    
    return final_result