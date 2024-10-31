from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from openai import OpenAI
import os
from dotenv import load_dotenv
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

# device = torch.device("mps" if torch.cuda.is_available() else "cpu")

# model = AutoModelForCausalLM.from_pretrained(
#     "Qwen/Qwen2-0.5B-Instruct",
#     torch_dtype="auto",
#     device_map="auto"
# ).to(device)

# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

def hq9_evaluation(answer):
        
    system_prompt = f"""
    # Role
    - You are a professional vegetable identifier who identifies vegetables.

    # Task
    - Given a single string of vegetable names without spaces, separate and identify each vegetable name.
    - The identified vegetables are actually Check if the vegetables are present.
    
    # Policy
    - Responses must be in Korean only, without any Chinese characters or mixed languages.
    - Provide the list of identified vegetables in the following JSON array format
    
    # Output Example
    {{
        "vegetable_list": ["채소1", "채소2", "채소3"...]
    }}
    
    # Output
    {{
        "vegetable_list": []
    }}
    """

    # messages = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": answer}
    # ]
    
    # text = tokenizer.apply_chat_template(
    #     messages,
    #     tokenize=False,
    #     add_generation_prompt=True
    # )
    
    # model_inputs = tokenizer([text], return_tensors="pt")

    # generated_ids = model.generate(
    #     model_inputs.input_ids,
    #     max_new_tokens=512
    # )

    # generated_ids = [
    #     output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    # ]
    
    # return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
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

    # 질문 생성 성공
    vegetable_list = result["vegetable_list"]
    num_vegetables = len(vegetable_list)

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

    return ({"score": score})