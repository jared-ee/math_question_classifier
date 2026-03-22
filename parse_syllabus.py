import os
from openai import OpenAI
import json
import re
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

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
    "learningOutcome": "",
    "loId": ""
  }}
]

Each item should represent one Learning Outcome, to be stated in the "learningOutcome" field.
The "strand", "subStrand" and "topic" are to be the Strand, Sub-Strand and Topic that Learning Outcome belongs to.
For the "topic" field, the Topic seen in the table may have an index in front of it (eg. "1. Numbers up to 10 000), but DO NOT include the index in the field (just "Numbers up to 10000").
For the "loId" field should be the following string: "{P}:" followed by the subStrand, followed by another ":", then finally the Ref number.

Syllabus:
{raw_text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-5.2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    cleaned = extract_json(content)
    converted = json.loads(cleaned)
    
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
