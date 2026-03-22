import os
from openai import OpenAI, AuthenticationError
import json
from json.decoder import JSONDecodeError
import re
from dotenv import load_dotenv
import sys

load_dotenv()

wd_api_key = os.getenv("WD_API_KEY")
if not wd_api_key:
    print("Error: Missing API key. Please set WD_API_KEY in .env")
    sys.exit(1)

client = OpenAI(
  api_key=os.getenv("WD_API_KEY"),
  base_url='https://ai-gateway.vercel.sh/v1'
)

def classify_question(question, syllabus):
    prompt = f"""
You are a math syllabus classifier.

Given a question, select the BEST matching learning outcome from the syllabus.

Return ONLY valid JSON in this format:
{{
  "strand": "...",
  "subStrand": "...",
  "topic": "...",
  "ref": "...",
  "learningOutcome": "...",
  "loId": "..."
}}

Syllabus:
{json.dumps(syllabus, indent=4)}

Question:
"{question}"
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-5.2",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
    except AuthenticationError:
        print("Error: Invalid or expired API key in .env")
        print("Please indicate a valid Vercel API key for OpenAI's GPT-5.2 model")
        sys.exit(1)

    output = response.choices[0].message.content
    try:
        json_output = json.loads(output)
    except JSONDecodeError:
        print("Model returned output in unexpected format. Please try again.")
        sys.exit(1)

    return json_output