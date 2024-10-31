from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

device = torch.device("mps" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-0.5B-Instruct",
    torch_dtype="auto",
    device_map="auto"
).to(device)

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")

def hq1_evaluation(answer):
        
    system_prompt = f"""
    # Role
    - You are a professional vegetable identifier who identifies vegetables.

    # Task

    # Policy

    # Output
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

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return