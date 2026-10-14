"""Small open-weight language model for one source-grounded extraction step."""
import re
from functools import lru_cache

MODEL_ID = "google/flan-t5-small"

@lru_cache(maxsize=1)
def load_model():
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
    model.eval()
    return tokenizer, model

def extract_multiplier(raw_text):
    """Ask a real instruction LLM to turn free-text wagering terms into a number."""
    import torch
    match = re.search(r"Wagering requirements:\s*(\d+(?:\.\d+)?\s*x)", raw_text, re.I)
    if not match:
        raise ValueError("No wagering phrase in source text")
    wagering_terms = match.group(1)
    tokenizer, model = load_model()
    prompt = f"What is the multiplier in the wagering requirement '{wagering_terms}'? Answer only with the number."
    encoded = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=96)
    with torch.no_grad():
        output = model.generate(**encoded, max_new_tokens=8, do_sample=False)
    generated = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    number = re.fullmatch(r"(\d+(?:\.\d+)?)\s*x?", generated, re.I)
    if not number:
        raise ValueError(f"Model output is not a numeric multiplier: {generated!r}")
    value = float(number.group(1))
    return int(value) if value.is_integer() else value
