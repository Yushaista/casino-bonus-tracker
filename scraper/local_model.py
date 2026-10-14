"""Small open-weight language model: no API key required."""
import re

MODEL_ID = "google/flan-t5-small"

def extract_multiplier(raw_text):
    """Convert unstructured bonus terms to one structured numeric field with an LLM."""
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
    model.eval()
    prompt = (
        "Extract the wagering multiplier as a number. Reply with only the number. "
        "Example: 'Wagering requirements: 20x' -> 20.\n" + raw_text
    )
    encoded = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        output = model.generate(**encoded, max_new_tokens=10, do_sample=False)
    generated = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    match = re.fullmatch(r"(\d+(?:\.\d+)?)\s*x?", generated, re.I)
    if not match:
        raise ValueError(f"Local model did not produce one multiplier: {generated!r}")
    number = float(match.group(1))
    return int(number) if number.is_integer() else number
