import requests
from classifier import classify_question
from evaluator import evaluate
import json
import sys

# Load syllabus
with open("syllabus.json") as f:
    syllabus = json.load(f)

# Fetch questions
#url = "https://api-v1.zyrooai.com/api/v1/math-classifier/interview/questions"
url = input("Enter the link the GET math questions from: ")
try:
    data = requests.get(url).json()["data"]
except Exception as e:
    print("Failed to GET questions. Please check if URL is valid. If valid, try again later.")
    sys.exit(1)

predictions = []
ground_truths = []

for item in data:
    pred = classify_question(item["question"], syllabus)

    predictions.append(pred)
    ground_truths.append(item["label"])

    print("\nQUESTION:", item["question"])
    print("PRED:", pred)
    print("GT:", item["label"])

accuracy = evaluate(predictions, ground_truths)

print("\nACCURACY:")
print(json.dumps(accuracy, indent=4))