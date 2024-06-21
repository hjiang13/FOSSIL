from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the CodeLlama model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-7b-hf")
model = AutoModelForSeq2SeqLM.from_pretrained("meta-llama/CodeLlama-7b-hf")

def summarize_code_with_codellama(snippet):
    inputs = tokenizer.encode("summarize: " + snippet, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=20, min_length=5, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

