import os
from openai import OpenAI
import json
import re
from dotenv import load_dotenv

load_dotenv()

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
  "learningOutcome": "...",
  "loId": "..."
}}

Syllabus:
{json.dumps(syllabus, indent=4)}

Question:
"{question}"
"""

    response = client.chat.completions.create(
        model="openai/gpt-5.2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    output = response.choices[0].message.content

    return json.loads(output)