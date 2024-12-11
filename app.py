from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import boto3
import os
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)

# Sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# AWS Configuration
S3_BUCKET = "sentiment-analysis-feedback-123"  # Replace with your S3 bucket name
DYNAMO_TABLE = "SentimentResults"  # Replace with your DynamoDB table name
REGION = "us-east-1"  # Modify based on your AWS region

# Initialize AWS clients
s3 = boto3.client("s3", region_name=REGION)
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(DYNAMO_TABLE)

# Ensure logs directory exists locally (if needed)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_to_s3_and_dynamodb(text, sentiment, score):
    """
    Log results to S3 and DynamoDB.
    """
    timestamp = datetime.now().isoformat()
    log_entry = f"{timestamp} - Text: {text} | Sentiment: {sentiment} | Score: {score}\n"

    # Log to S3
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"logs/{timestamp}.txt",
        Body=log_entry
    )

    # Log to DynamoDB, convert score to Decimal
    table.put_item(
        Item={
            "Timestamp": timestamp,
            "Text": text,
            "Sentiment": sentiment,
            "Score": Decimal(str(score))  # Convert score to Decimal
        }
    )

# Route to display the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route for sentiment analysis
@app.route("/analyze", methods=["POST"])
def analyze():
    # Extract text from the form data
    text = request.form.get("text")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Perform sentiment analysis
    result = sentiment_analyzer(text)[0]
    sentiment = result["label"]
    score = result["score"]

    # Log the result to S3 and DynamoDB
    log_to_s3_and_dynamodb(text, sentiment, score)

    # Return the analysis result
    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "score": float(score)  # Convert Decimal back to float when sending response
    })

# Route to fetch logs from S3
@app.route("/logs")
def view_logs():
    # List objects in the S3 logs directory
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix="logs/")
    log_files = []

    # Get the log files from S3
    if 'Contents' in response:
        log_files = [file['Key'] for file in response['Contents']]

    logs = []
    for log_file in log_files:
        # Get the log file content from S3
        log_content = s3.get_object(Bucket=S3_BUCKET, Key=log_file)
        logs.append(log_content['Body'].read().decode('utf-8'))

    return render_template("logs.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
