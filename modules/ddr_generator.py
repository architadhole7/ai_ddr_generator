import random
import re


# 🔹 Clean noisy extracted text
def clean_text(text):
    remove_words = [
        "Negative side Description",
        "Positive side Description",
        "photographs",
        "Photo",
        "Inputs"
    ]

    for w in remove_words:
        text = re.sub(w, "", text, flags=re.IGNORECASE)

    # 🔥 FIX BROKEN e.g patterns (ALL cases)
    text = re.sub(r"\(e\s*[,\.]?\s*", "(e.g., ", text)
    text = re.sub(r"e\s*\n\s*,", "e.g.,", text)

    return text.strip()


# 🔹 Infer cause (fallback)
def infer_cause(observation):
    obs = observation.lower()

    water_causes = [
        "Possible water ingress due to plumbing leakage",
        "Likely due to waterproofing failure or seepage",
        "Moisture intrusion from adjacent wet areas",
        "Possible concealed pipe leakage inside wall/floor"
    ]

    structural_causes = [
        "Possible structural stress or settlement",
        "Material fatigue or external load impact",
        "Cracks due to thermal expansion or shrinkage"
    ]

    material_causes = [
        "Poor installation or material degradation",
        "Wear and tear over time",
        "Surface damage due to environmental exposure"
    ]

    if any(w in obs for w in ["leak", "damp", "seepage", "water"]):
        return random.choice(water_causes)

    elif any(w in obs for w in ["crack", "beam", "column"]):
        return random.choice(structural_causes)

    elif any(w in obs for w in ["tile", "paint", "rust"]):
        return random.choice(material_causes)

    return "Not Available"


# 🔹 Smart recommendation generator
def generate_recommendation(observation):
    obs = observation.lower()

    # 🔴 Leakage
    if "leak" in obs:
        return [
            "Identify exact source of leakage",
            "Repair plumbing or sealing defects",
            "Test repaired area to confirm no leakage",
            "Restore damaged surfaces after repair"
        ]

    # 🟠 Dampness
    elif any(w in obs for w in ["damp", "seepage", "moisture"]):
        options = [
            [
                "Identify source of moisture ingress",
                "Apply waterproofing treatment",
                "Allow area to dry completely",
                "Repaint or refinish affected surfaces"
            ],
            [
                "Inspect area to detect moisture entry point",
                "Carry out waterproofing repairs",
                "Ensure complete drying of affected surface",
                "Restore surface finishes after drying"
            ],
            [
                "Investigate dampness source",
                "Fix leakage or seepage issues",
                "Dry affected zone thoroughly",
                "Repair damaged wall finishes"
            ]
        ]

        return random.choice(options)

    # 🟡 Structural
    elif any(w in obs for w in ["crack", "column", "beam"]):
        return [
            "Inspect structural elements for damage",
            "Repair cracks using suitable materials",
            "Assess need for structural reinforcement",
            "Monitor for further movement"
        ]

    # 🔵 Material
    elif any(w in obs for w in ["tile", "paint", "rust"]):
        return [
            "Inspect damaged materials",
            "Repair or replace affected components",
            "Ensure proper installation and sealing",
            "Apply finishing or protective coating"
        ]

    # ⚪ Default
    return [
        "Inspect the affected area",
        "Identify root cause",
        "Carry out necessary repairs",
        "Monitor condition after repair"
    ]


# 🔹 MAIN FUNCTION
def generate_ddr(final_obs):
    if not final_obs:
        return {
            "summary": "Not Available",
            "observations": [],
            "additional_notes": "Not Available",
            "missing_info": "Not Available"
        }

    observations = []
    conflict_notes = []
    seen = set()
    missing_areas = set()

    for obs in final_obs:
        area = obs.get("area") 
        issue = obs.get("issue") or "Not Available"
        details = obs.get("details") or "Not Available"
        analysis = obs.get("analysis") or ""

        # 🔍 Missing detection
        # 🔍 Missing detection (improved)
        if area == "Not Available":
            missing_areas.add("Unknown Area")

        if issue == "Not Available":
            missing_areas.add(area)

        if details == "Not Available":
            missing_areas.add(area)

        # ⚠️ Conflict detection
        if "leakage" in details.lower() and "no leakage" in details.lower():
            conflict_notes.append(f"Conflicting leakage info in {area}")

        # 🧹 Clean observation
        raw_text = details if details != "Not Available" else issue
        observation_text = clean_text(raw_text)

        # 🔥 Default recommendation
        recommendation = generate_recommendation(observation_text)

        # 🔥 Default cause
        cause = "Not Available"

        # 🤖 AI parsing
        if analysis:
            analysis = analysis.replace("**", "")

            # Extract cause
            if "Root Cause:" in analysis:
                cause_part = analysis.split("Root Cause:")[-1]
                cause = cause_part.split("Severity:")[0].strip() if "Severity:" in cause_part else cause_part.strip()

            # Extract recommendation (only if useful)
            if "Recommendation:" in analysis:
                recommendation_text = analysis.split("Recommendation:")[-1].strip().lower()

                if not any(x in recommendation_text for x in [
                    "further inspection",
                    "necessary repair",
                    "not available",
                    "inspection recommended"
                ]):
                    recommendation_text = recommendation_text.replace("\n", " ")
                    recommendation_text = re.sub(r"\d+\.", "", recommendation_text)

                    cleaned = [
                        point.strip()
                        for point in recommendation_text.split(".")
                        if point.strip() and len(point.strip()) > 5
                    ]

                    if cleaned:
                        recommendation = [p.capitalize() for p in cleaned]

        # 🔁 fallback cause
        if cause == "Not Available":
            cause = infer_cause(observation_text)

        # ⚡ Severity
        text = (issue + " " + details).lower()

        if any(word in text for word in ["leak", "crack", "structural"]):
            severity = "High"
        elif any(word in text for word in ["damp", "moisture"]):
            severity = "Medium"
        else:
            severity = "Low"

        # 🧹 Remove duplicates
        key = (area, observation_text)
        if key in seen:
            continue
        seen.add(key)

        observations.append({
            "area": area,
            "observation": observation_text,
            "severity": severity,
            "cause": cause,
            "recommendation": recommendation,
            "images": obs.get("images", [])
        })

    # 🧾 Summary
    summary = f"{len(observations)} issues were identified during inspection."

    # 📌 Missing info
    if missing_areas:
        missing_info = "Details missing for: " + ", ".join(missing_areas)
    else:
        missing_info = "Not Available"

    # ⚠️ Notes
    additional_notes = "Report generated strictly from provided documents."
    if conflict_notes:
        additional_notes += " Conflicts observed: " + ", ".join(conflict_notes)

    return {
        "summary": summary,
        "observations": observations,
        "additional_notes": additional_notes,
        "missing_info": missing_info
    }