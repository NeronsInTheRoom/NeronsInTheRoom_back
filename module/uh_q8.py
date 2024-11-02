from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
import json

device = torch.device("mps" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-0.5B-Instruct",
    torch_dtype="auto",
    device_map="auto"
).to(device)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

# 미리 정의된 객체 리스트
object_list = {
    "item1": "시계",
    "item2": "열쇠",
    "item3": "도장",
    "item4": "연필",
    "item5": "동전"
}

def hq8_evaluation(answer):
    
    # # NER 모델과 토크나이저 로드
    # model_name = "KoichiYasuoka/roberta-large-korean-upos"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModelForTokenClassification.from_pretrained(model_name)
    # ner = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    
    # # NER을 통한 단어 추출
    # entities = ner(answer)
    # extracted_words = [entity["word"] for entity in entities]
    
    # # 필요한 객체 리스트
    # object_list = ["시계", "열쇠", "도장", "연필", "동전"]
    
    # # 필요한 객체 필터링
    # matched_words = [word for word in extracted_words if word in object_list]
    # print(f"@@@@@@@@@@@@@@@: {matched_words}")
    
    # # 점수 계산: 일치하는 객체 수만큼 점수 부여
    # score = len(matched_words)
    
    system_prompt = f"""
    
    # Role
    You are a language model that identifies individual Korean words within a continuous string of text.

    # Task
    Given a single string of Korean object names written together without spaces, separate each word and list them separated by commas.
    
    # Policy
    - Responses must be in Korean only, without any Chinese characters or mixed languages.
    - Provide the list of identified vegetables in the following JSON array format
    
    # Output
    {{
        "answer_list": []
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

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response_content = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    result = json.loads(response_content)
    print(f"감지된 언어: {result}")
    
    # 점수 계산
    score = sum(1 for answer in result["answer_list"] if answer in object_list.values())
   
    return {"score": score}