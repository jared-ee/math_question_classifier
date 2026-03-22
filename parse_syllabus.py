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

def extract_json(text):
    # Remove markdown if present
    text = text.strip()

    # Extract JSON array
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group(0)

    return text

def parse_syllabus(raw_text, P):
    prompt = f"""
Convert the following syllabus table into structured JSON.

Structure:
[
  {{
    "strand": "",
    "subStrand": "",
    "topic": "",
    "ref": "",
    "learningOutcome": "",
    "loId": ""
  }}
]

Each item should represent one Learning Outcome, to be stated in the "learningOutcome" field.
The "strand", "subStrand", "topic" and "ref" are to be the Strand, Sub-Strand, Topic and Ref number that Learning Outcome belongs to.
For the "topic" field, the Topic seen in the table may have an index in front of it (eg. "1. Numbers up to 10 000), but DO NOT include the index in the field (just "Numbers up to 10000").
For the "loId" field should be the following string: "{P}:" followed by the subStrand, followed by another ":", then finally the Ref number.

Syllabus:
{raw_text}
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

    content = response.choices[0].message.content
    cleaned = extract_json(content)
    try:
        converted = json.loads(cleaned)
    except JSONDecodeError:
        print("Model returned output in unexpected format. Please try again.")
        sys.exit(1)
    
    return converted

combined = []
data_folder = "data"
for data_file in os.listdir(data_folder):
    filepath = os.path.join(data_folder, data_file)
    if data_file.endswith("_syllabus.txt"):
        level = data_file.replace("_syllabus.txt", "")

        with open(filepath, 'r', encoding='utf-8') as file:
            raw_text = file.read()

        data = parse_syllabus(raw_text, level)
        combined += data

with open('syllabus.json', 'w') as f:
    json.dump(combined, f, indent=4)
