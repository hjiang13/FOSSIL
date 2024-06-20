from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the CodeBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/codebert-base")

def summarize_code_with_codebert(snippet):
    inputs = tokenizer.encode("summarize: " + snippet, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=10, min_length=3, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
