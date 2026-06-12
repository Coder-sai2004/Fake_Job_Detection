# services/reason_generator.py

import json
from services.gemini_service import ask_gemini


def generate_job_analysis(job_description, prediction):
    """
    Generate risk score and reasons for a job posting.

    Returns:
    {
        "risk_score": int,
        "risk_level": str,
        "reasons": list
    }
    """

    prompt = f"""
You are an expert job fraud analyst.

Analyze the following job posting and based on real//fake job ,explain the prediction and give reasons why it is fake or real.

ML Model Prediction:
{prediction}

Return ONLY valid JSON.

Required format:

{{
    "risk_score": 0,
    "reasons": [
        "reason 1",
        "reason 2",
        "reason 3"
    ]
}}

Rules:
- risk_score must be between 0 and 100
- Give 3 to 5 reasons
- No markdown
- No explanation outside JSON
- Return valid JSON only
- Each reason must be under 10 words
- Use short bullet-style phrases
- Do not write full sentences

Job Posting:
{job_description}
"""

    try:
        response = ask_gemini(prompt)

        # Clean Gemini response if wrapped in markdown
        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "").replace("```", "").strip()

        elif response.startswith("```"):
            response = response.replace("```", "").strip()

        data = json.loads(response)

        risk_score = data.get("risk_score", 50)

        # Ensure score stays within range
        risk_score = max(0, min(100, risk_score))

        # Calculate risk level
        if risk_score <= 30:
            risk_level = "Low"
        elif risk_score <= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": data.get(
                "reasons",
                ["Unable to generate detailed analysis"]
            )
        }

    except Exception as e:
        print("Reason Generator Error:", e)

        return {
            "risk_score": 50,
            "risk_level": "Medium",
            "reasons": [
                "Unable to generate analysis"
            ]
        }