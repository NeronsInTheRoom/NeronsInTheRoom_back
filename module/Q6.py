from dotenv import load_dotenv
from openai import OpenAI
from data import questions, correctAnswer
import os
import json
import re

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

def is_numbers_only(text):
    # 숫자와 구분자(쉼표, 공백)만 있는지 확인
    cleaned_text = re.sub(r'[,\s]', '', text)
    return cleaned_text.isdigit()

def compare_number_sequence(user_answer, correct_answer):
    # 구분자를 제거하고 숫자만 추출
    user_nums = ''.join(re.findall(r'\d+', user_answer))
    correct_nums = ''.join(re.findall(r'\d+', correct_answer))
    return user_nums == correct_nums

async def Q6Score(text: str, questionNumber):
    # 숫자로만 이루어진 응답인지 확인
    if is_numbers_only(text):
        # 해당하는 정답 가져오기
        correct = next((a["value"] for a in correctAnswer if a["key"] == questionNumber), None)
        if correct is None:
            raise ValueError(f"{questionNumber} 정답을 찾을 수 없습니다.")
        
        # 순서를 포함한 정확한 숫자 비교
        score = 1 if compare_number_sequence(text, correct) else 0
        return {
            "score": str(score),
            "answer": text
        }

    # 텍스트가 포함된 경우 기존 LLM 로직 실행
    if questionNumber == "Q6":
        q6_question = next((q["value"] for q in questions if q["key"] == "Q6"), None)
        if q6_question is None:
            raise ValueError("Q6 질문을 찾을 수 없습니다.")
        q6_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q6"), None)
        if q6_answer is None:
            raise ValueError("Q6 정답을 찾을 수 없습니다.")

        prompt = f"""

        #Role            
        - You have a scoring system that evaluates your answers to user questions. 
        - You are an expert in analyzing Korean STT (Speech-to-Text) responses where numbers might be transcribed as Korean words.

        # Task
        You are an expert in analyzing and scoring user responses based on understanding sentence structure and context.
        You are an expert in analyzing and scoring user responses with focus on exact number sequence matching.
        You must extract numbers from natural language responses and check if they match the answer sequence.   
        The result must be returned only as the number 1 for correct answers or 0 for incorrect answers.
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
        q6_1_question = next((q["value"] for q in questions if q["key"] == "Q6-1"), None)
        if q6_1_question is None:
            raise ValueError("Q6-1 질문을 찾을 수 없습니다.")
        q6_1_answer = next((a["value"] for a in correctAnswer if a["key"] == "Q6-1"), None)
        if q6_1_answer is None:
            raise ValueError("Q6-1 정답을 찾을 수 없습니다.")

        prompt = f"""
            
        # Role
        - You have a scoring system that evaluates your answers to user questions. The user's answer is checked to see if it fits the question and given a score.
        - You are an expert in analyzing Korean STT (Speech-to-Text) responses where numbers might be transcribed as Korean words.

        # Task
        You are an expert in analyzing and scoring user responses based on understanding sentence structure and context.
        You are an expert in analyzing and scoring user responses with focus on exact number sequence matching.
        You must extract numbers from natural language responses and check if they match the answer sequence.
        You must review the question and correct answer, then evaluate whether the user's response matches the answer.
        The result must be returned only as the number 1 for correct answers or 0 for incorrect answers.

        - You must correctly interpret numbers that may be transcribed in Korean, focusing on common STT conversion patterns:
           * "이" at the start of a sequence often means "2" when followed by other numbers
           * "이랑", "이,", "이 " when followed by numbers are likely meant to be "2"
           * Numbers may be connected with Korean words like "랑", "그리고", "와", "하고"

        - You must check if the user's answer contains the same numbers as the correct answer AND in the exact same order.
        - For example, if the correct answer is "9,2,5,3":
           * "9,2,5,3" = correct (same numbers and order)
           * "9253" = correct (same numbers and order)
           * "9 2 5 3" = correct (same numbers and order)
           * "구,이,오,삼" = correct (Korean number words)
           * "구랑 이랑 오랑 삼" = correct (Korean with connectors)
           * "구랑이랑 오랑 3" = correct (Korean with connectors)
           * "구 그리고 이 그리고 오 그리고 삼" = correct (Korean with different connectors)
           * "3,5,2,9" = incorrect (wrong order)
           * "3,2,5,9" = incorrect (wrong order)
           * "9,5,2,3" = incorrect (wrong numbers)

        - Important Context Rules:
           * Only interpret "이" as "2" when:
                - It appears in a sequence with other numbers
                - It's used with number-connecting words (랑, 그리고, 와, 하고)
           * Do not convert "이" to "2" when:
                - It's part of other Korean words
                - It's used in a different context
           * The order of numbers must match exactly, even if all the correct numbers are present
           * Spaces, commas, or other separators do not affect the score as long as the numbers and their order are correct

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
        result = json.loads(response_content)
        return result
    except json.JSONDecodeError:
        print("응답이 JSON 형식이 아닙니다. 응답 내용:", response_content)
        return None