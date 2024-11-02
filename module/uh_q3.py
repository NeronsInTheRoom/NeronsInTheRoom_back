from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
import time
import re

device = torch.device("mps" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-0.5B-Instruct",
    torch_dtype="auto",
    device_map="auto"
).to(device)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

def hq3_evaluation(location, answer):
    
    # 시간 기록 시작 (5초)
    start_time = time.time()
    
    system_prompt = f"""
    
    # Role
    - You are an expert location comparer.

    # Task
    - First, the user's actual location ({location}).
    - Second, the location answered by the user ({answer}).
    - Third, compare {location} and {answer}.
    - Fourth, we analyze whether the {answer} location the user answered is related to the user's actual location {location}
    - Fifth, if there is a relationship between the two in the previous step, assign 2 to the "score" of the JSON type.
    - Sixth, if there is no relationship, assign 0 to “score”.
    
    # Output
    - Return only in JSON format:
    {{
        "score":
    }}
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": answer}
    ]
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    model_inputs = tokenizer([text], return_tensors="pt")
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    response_content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(f"@@@@@@@@@@@@@: {response_content}")
    
    # 정규식으로 "score" 값을 추출해 기본값으로 설정
    match = re.search(r'{"score":\s*(\d+)}', response_content)
    score = int(match.group(1)) if match else 0
    
    # 5초 이내 여부 확인
    elapsed_time = time.time() - start_time
    if elapsed_time > 5 and score == 2:
        score = 1  # 연관성이 있지만 5초가 초과되면 1점 부여
        
    return {"score": score}