from transformers import pipeline

# Initialize the Hugging Face sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Sample text for testing the model
sample_text = "I love this project, it's amazing!"

# Get sentiment analysis result
result = sentiment_analyzer(sample_text)

# Print the result
print(f"Text: {sample_text}")
print(f"Sentiment: {result[0]['label']}")
print(f"Score: {result[0]['score']}")
