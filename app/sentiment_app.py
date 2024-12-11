import os
from datetime import datetime
from transformers import pipeline

# Directories
LOG_DIR = "../logs"
BATCH_FILE = "../input_texts.txt"

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Load the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def log_results(text, sentiment, score):
    """
    Log sentiment analysis results to a file.
    """
    log_file = os.path.join(LOG_DIR, "analysis_logs.txt")
    with open(log_file, "a") as file:
        file.write(f"{datetime.now()} - Text: {text} | Sentiment: {sentiment} | Score: {score:.4f}\n")

def analyze_text(text):
    """
    Analyze a single text for sentiment.
    """
    result = sentiment_analyzer(text)[0]
    sentiment = result["label"]
    score = result["score"]
    print(f"Text: {text}\nSentiment: {sentiment}\nScore: {score:.4f}\n")
    log_results(text, sentiment, score)

def batch_process():
    """
    Batch process texts from a file.
    """
    if not os.path.exists(BATCH_FILE):
        print(f"No batch file found at {BATCH_FILE}. Skipping batch processing.")
        return

    print(f"Processing texts from {BATCH_FILE}...")
    with open(BATCH_FILE, "r") as file:
        texts = file.readlines()

    for text in texts:
        text = text.strip()
        if text:  # Skip empty lines
            analyze_text(text)

def main():
    """
    Main application loop.
    """
    print("Welcome to the Sentiment Analysis App!")
    while True:
        user_input = input("Enter text ('batch' for batch processing, 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break
        elif user_input.lower() == "batch":
            batch_process()
        else:
            analyze_text(user_input)

if __name__ == "__main__":
    main()
