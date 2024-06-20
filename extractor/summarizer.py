from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_code_with_huggingface(snippet):
    summary = summarizer(snippet, max_length=10, min_length=5, do_sample=False)
    return summary[0]['summary_text']
