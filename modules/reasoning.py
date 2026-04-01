import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


#  Generalized fallback logic
def infer_cause(observation):
    obs = observation.lower()

    if any(w in obs for w in ["leak", "seepage", "water", "damp", "moisture", "efflorescence"]):
        return "Possible water ingress due to plumbing leakage or waterproofing failure"

    elif any(w in obs for w in ["crack", "fracture", "beam", "column", "structural"]):
        return "Possible structural stress, settlement, or material fatigue"

    elif any(w in obs for w in ["fire", "burn", "smoke", "heat"]):
        return "Possible fire-related damage or excessive heat exposure"

    elif any(w in obs for w in ["wire", "electrical", "short circuit", "spark"]):
        return "Possible electrical fault or wiring issue"

    elif any(w in obs for w in ["tile", "plaster", "paint", "rust", "corrosion"]):
        return "Possible material degradation or poor installation quality"

    return "Not Available"


def infer_severity(text):
    text = text.lower()

    if any(w in text for w in ["leak", "fire", "crack", "structural", "short circuit"]):
        return "High"

    elif any(w in text for w in ["damp", "moisture", "corrosion", "tile"]):
        return "Medium"

    return "Low"


def enrich_observations(observations):
    enriched = []

    #  LIMIT AI CALLS because of limited credits
    MAX_AI_CALLS = 5
    ai_calls = 0

    for obs in observations:
        text = f"{obs.get('issue', '')} {obs.get('details', '')}"

        #  TRY AI (only few times)
        if ai_calls < MAX_AI_CALLS:
            prompt = f"""
You are a building inspection expert.

Given:
Area: {obs.get('area')}
Issue: {obs.get('issue')}
Details: {obs.get('details')}

Return:
Root Cause: ...
Severity: ...
Recommendation: ...

Rules:
- Do NOT invent facts
- Keep it simple
"""

            try:
                response = model.generate_content(prompt)
                result = response.text

                obs["analysis"] = result
                ai_calls += 1

            except Exception as e:
                print("Gemini reasoning error:", str(e))

                #  fallback
                obs["analysis"] = f"""
Root Cause: {infer_cause(text)}
Severity: {infer_severity(text)}
Recommendation: Further inspection and necessary repair recommended.
"""

        else:
            #  ALWAYS fallback after limit
            obs["analysis"] = f"""
Root Cause: {infer_cause(text)}
Severity: {infer_severity(text)}
Recommendation: Further inspection and necessary repair recommended.
"""

        enriched.append(obs)

    return enriched
