import google.generativeai as genai
import json
import re
import os

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# 🔹 Prompt Builder
def build_prompt(text, source):
    return f"""
You are an AI system that extracts structured data.

Return ONLY valid JSON. No explanation. No text outside JSON.

Format:
[
  {{
    "area": "",
    "issue": "",
    "details": "",
    "source": "{source}"
  }}
]

Rules:
- Do NOT add any text before or after JSON
- Do NOT explain anything
- If data missing → use "Not Available"
- Extract only meaningful observations (ignore junk)
- Keep output strictly in JSON array format

Text:
{text}
"""


# 🔹 Gemini Extraction
def extract_with_gemini(text, source):
    try:
        # Limit text to avoid API failure
        text = text[:8000]

        prompt = build_prompt(text, source)
        response = model.generate_content(prompt)

        raw_text = response.text

        # Clean markdown formatting if any
        cleaned = re.sub(r"```json|```", "", raw_text).strip()

        data = json.loads(cleaned)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:
        print("Gemini Extraction Error:", str(e))
        return []


# 🔹 Main Function (AI + fallback)
def extract_observations(text, type):
    try:
        observations = extract_with_gemini(text, type)

        # If AI fails → fallback
        if not observations or len(observations) == 0:
            raise Exception("AI returned empty")

        return observations

    except Exception as e:
        print("AI FAILED → using fallback extraction")

        return basic_extraction(text)


# 🔹 Fallback Extraction (rule-based)
def basic_extraction(text):
    observations = []

    lines = text.split("\n")

    for line in lines:
        l = line.lower()

        if "dampness" in l or "leakage" in l:
            observations.append({
                "area": extract_area(l),
                "issue": "Dampness/Leakage",
                "details": line.strip(),
                "analysis": "Possible water seepage due to plumbing or waterproofing issue"
            })

    return observations


# 🔹 Area Detection
def extract_area(line):
    if "hall" in line:
        return "Hall"
    if "bedroom" in line:
        return "Bedroom"
    if "kitchen" in line:
        return "Kitchen"
    if "bathroom" in line or "wc" in line:
        return "Bathroom/WC"
    if "parking" in line:
        return "Parking Area"

    return "Not Available"