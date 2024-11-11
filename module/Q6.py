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

async def Q6Score(text: str, questionNumber):

    if questionNumber == "Q6":
        # Q5 문제와 정답 가져오기
        q6_question = next((q["value"] for q in questions if q["key"] == "Q6"), None)
        if q6_question is None:
            raise ValueError("Q6 질문을 찾을 수 없습니다.")
        q6_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q6"), None)
        if q6_answer is None:
            raise ValueError("Q6 정답을 찾을 수 없습니다.")

        prompt = f"""
            
        - You have a scoring system that evaluates your answers to user questions. 
        - You are an expert in analyzing Korean STT (Speech-to-Text) responses where numbers might be transcribed as Korean words.


        You are an expert in analyzing and scoring user responses based on understanding sentence structure and context.
        You are an expert in analyzing and scoring user responses with focus on exact number sequence matching.
        You must extract numbers from natural language responses and check if they match the answer sequence.
        The result must be returned only as the number 1 for correct answers or 0 for incorrect answers.

        # Task
        - You must correctly interpret numbers that may be transcribed in Korean, focusing on common STT conversion patterns:
            * "이" at the start of a sequence often means "2" when followed by other numbers
            * "이랑", "이,", "이 " when followed by numbers are likely meant to be "2"
        
        - For example, if the correct answer is "2,8,6":
            * "2,8,6" = correct
            * "286" = correct
            * "이,8,6" = correct (STT converted "2" to "이")
            * "이랑 8이랑 6" = correct (STT conversion with Korean connectors)
            * "이 8 6" = correct (STT conversion with spaces)
            * "이 그리고 8 그리고 6" = correct
            * "8,6,이" = incorrect (wrong order)
            * "6,8,이" = incorrect (wrong order)
            * "이,8,3" = incorrect (wrong number)

        - Important Context Rules:
            * Only interpret "이" as "2" when:
                - It appears in a sequence with other numbers
                - It's used with number-connecting words (랑, 그리고, 와, 하고)
            * Do not convert "이" to "2" when:
                - It's part of other Korean words
                - It's used in a different context

        # Context
        - Question: {q6_question} 
        - Correct Answer: {q6_answer}
        - User's Response: {text}

        # Output
        {{
            "score":"",
            "answer": "{text}"
        }}
        """
    
    elif questionNumber == "Q6-1":
        # Q5-1 문제와 정답 가져오기
        q6_1_question = next((q["value"] for q in questions if q["key"] == "Q6-1"), None)
        if q6_1_question is None:
            raise ValueError("Q6-1 질문을 찾을 수 없습니다.")
        q6_1_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q6-1"), None)
        if q6_1_answer is None:
            raise ValueError("Q6-1 정답을 찾을 수 없습니다.")

        prompt = f"""
            
        # Role
        - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.

        You are an expert in analyzing and scoring user responses based on understanding sentence structure and context.
        You are an expert in analyzing and scoring user responses with focus on exact number sequence matching.
        You must review the question and correct answer, then evaluate whether the user's response matches the answer.
        The result must be returned only as the number 1 for correct answers or 0 for incorrect answers.

        # Task
        - You must check if the user's answer contains the same numbers as the correct answer AND in the exact same order.
        - For example, if the correct answer is "9,2,5,3":
        * "9,2,5,3" = correct (same numbers and order)
        * "9253" = correct (same numbers and order)
        * "9 2 5 3" = correct (same numbers and order)
        * "3,5,2,9" = incorrect (wrong order)
        * "3,2,5,9" = incorrect (wrong order)
        * "9,5,2,3" = incorrect (wrong number)
        - The order of numbers must match exactly, even if all the correct numbers are present.
        - Spaces, commas, or other separators do not affect the score as long as the numbers and their order are correct.

        # Context
        - Question: {q6_1_question} 
        - Correct Answer: {q6_1_answer}
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