from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

# device = torch.device("mps" if torch.cuda.is_available() else "cpu")

# model = AutoModelForCausalLM.from_pretrained(
#     "Qwen/Qwen2-0.5B-Instruct",
#     torch_dtype="auto",
#     device_map="auto"
# ).to(device)

# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

def hq1_evaluation(age, answer):
    
    # 문자열에서 숫자만 추출
    age_num = int(re.sub(r'\D', '', age))
    answer_num = int(re.sub(r'\D', '', answer))
    print(f"age: {age}, answer: {answer}")
    print(f"age_num: {age_num}, answer_num: {answer_num}")
    print(f"age_num: {type(age_num)}, answer_num: {type(answer_num)}")
    
    # 실제 나이 - 답변 나이 = 절대값 구하기
    difference = abs(age_num - answer_num)
    print(f"절대값: {difference}")
    res_abs = 1 if difference <= 2 else 0
    
    # system_prompt = f"""
    # # Role
    # You are a dementia assessment rater.

    # # Task
    # - Evaluation order:
    #     First, the user's actual age is {age_num}.
    #     Second, the age at which the user answered is {answer_num}.
    #     Third, subtract the two values and change them to absolute values.
    #     Fourth, if the value is less than 2, 1 point is given, and if it is more than 2, 0 points are given.
    # - Respond only with a single integer: "1" or "0" based on the criteria above.

    # # Policy
    # - Only respond with the score: "1" or "0".
    # - Do not provide explanations or any text other than the score.
    # - The response must be in JSON output format.
    # - The score is placed in the "score" field of the JSON output.

    # # Output
    # {{
    #     "score":
    # }}
    # """

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
    
    # response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return {"score": res_abs}
    
# 1, 2, 3, 8, 9 평가
# 1: 나이 정보 받아야됨
# 2: 오늘 날짜 받아야됨
# 3: ?
# 8: 이미지 랜덤 5개 정보 필요, 순서 상관 없음, 1개 당 점수 1점
# 9: 채소 이름 갯수에 따른 점수 부여