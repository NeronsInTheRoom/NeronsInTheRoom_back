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

async def Q5Score(text: str, questionNumber):

    if questionNumber == "Q5":
        # Q5 문제와 정답 가져오기
        q5_question = next((q["value"] for q in questions if q["key"] == "Q5"), None)
        if q5_question is None:
            raise ValueError("Q5 질문을 찾을 수 없습니다.")
        q5_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q5"), None)
        if q5_answer is None:
            raise ValueError("Q5 정답을 찾을 수 없습니다.")

        prompt = f"""
            
        # Role
        - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

        You are an expert in analyzing and scoring user responses based on understanding sentence structure and context.
        You must review the question and correct answer, then evaluate whether the user's response matches the answer.
        You should check for similar numbers in the user's response (e.g., 9, 10, 13) and accept answers that were intended to be 93 but may have been typed incorrectly.
        The result must be returned only as the number 1 for correct answers or 0 for incorrect answers.

        # Context
        - Question: {q5_question} 
        - Correct Answer: {q5_answer}
        - User's Response: {text}

        # Output
        {{
            "score":"",
            "answer": "{text}"
        }}
        """
    
    elif questionNumber == "Q5-1":
        # Q5-1 문제와 정답 가져오기
        q5_1_question = next((q["value"] for q in questions if q["key"] == "Q5-1"), None)
        if q5_1_question is None:
            raise ValueError("Q5-1 질문을 찾을 수 없습니다.")
        q5_1_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q5-1"), None)
        if q5_1_answer is None:
            raise ValueError("Q5-1 정답을 찾을 수 없습니다.")

        prompt = f"""
            
        # Role
        - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

        You are an expert in analyzing and scoring user responses based on understanding sentence structure and context.
        You must review the question and correct answer, then evaluate whether the user's response matches the answer.
        You should check for similar numbers in the user's response (e.g., 8, 10, 6) and accept answers that were intended to be 93 but may have been typed incorrectly.
        The result must be returned only as the number 1 for correct answers or 0 for incorrect answers.

        # Context
        - Question: {q5_1_question} 
        - Correct Answer: {q5_1_answer}
        - User's Response: {text}

        # Output
        {{
            "score":"",
            "answer": "{text}"
        }}
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