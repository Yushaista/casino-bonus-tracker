"""Tiny public instruction-tuned LLM for extracting one numeric bonus term."""
import re
from functools import lru_cache

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

@lru_cache(maxsize=1)
def load_model():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
    model.eval()
    return tokenizer, model

def extract_multiplier(raw_text):
    """Use a genuine local instruction model, with caller-side evidence checks."""
    import torch
    match = re.search(r"Wagering requirements:\s*(\d+(?:\.\d+)?\s*x)", raw_text, re.I)
    if not match:
        raise ValueError("No wagering requirement in source text")
    wagering_terms = match.group(1)
    tokenizer, model = load_model()
    messages = [
        {"role": "system", "content": "Extract the wagering multiplier. Reply with ONLY the number, not words."},
        {"role": "user", "content": f"Wagering requirement: {wagering_terms}"},
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    encoded = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**encoded, max_new_tokens=12, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    answer = tokenizer.decode(output[0][encoded.input_ids.shape[1]:], skip_special_tokens=True).strip()
    found = re.fullmatch(r"(\d+(?:\.\d+)?)\s*x?", answer, re.I)
    if not found:
        raise ValueError(f"Local LLM returned nonnumeric answer: {answer!r}")
    number = float(found.group(1))
    return int(number) if number.is_integer() else number
