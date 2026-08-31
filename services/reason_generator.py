# services/reason_generator.py
#
# Generates human-readable reasons explaining the fraud prediction.
# Uses Gemini to interpret the ML result — but Gemini is clearly
# the interpreter, not the source of truth.
#
# If Gemini is unavailable, returns honest fallback reasons
# derived from the ML prediction label rather than inventing details.

import json
from services.gemini_service import ask_gemini, get_friendly_error_message


_FALLBACK_REASONS_FAKE = [
    "ML model flagged high-risk linguistic patterns in this posting.",
    "Text similarity to known fraudulent job postings is elevated.",
    "Verify company identity independently before responding.",
    "AI analysis was unavailable — treat ML prediction with caution.",
]

_FALLBACK_REASONS_REAL = [
    "ML model found this posting consistent with legitimate job descriptions.",
    "Text patterns align with genuine employment opportunities.",
    "No obvious fraud indicators detected by the ML classifier.",
    "AI analysis was unavailable — ML-only prediction shown.",
]


def generate_job_analysis(job_description: str, prediction: str) -> dict:
    """
    Generate risk score and reasons for a job posting.

    Returns:
    {
        "risk_score":       int,
        "risk_level":       str,
        "reasons":          list[str],
        "ai_unavailable":   bool
    }
    """

    prompt = f"""
You are an expert job fraud analyst.

Analyze the following job posting. The ML model predicted: {prediction}

Explain specifically WHY this posting is likely {prediction.lower()}.
Base your reasoning only on what is actually present in the text.

Job Posting:
{job_description}

Return ONLY valid JSON in this exact format:

{{
    "risk_score": 0,
    "reasons": [
        "reason 1",
        "reason 2",
        "reason 3"
    ]
}}

Rules:
- risk_score must be between 0 and 100 (higher = more likely fake)
- Give 3 to 5 reasons grounded in the actual text
- No markdown
- No explanation outside JSON
- Return valid JSON only
- Each reason must be under 15 words
- Use short, specific bullet-style phrases
- Do NOT invent details not present in the posting
"""

    try:
        response = ask_gemini(prompt)

        # ------------------------------------------------------------------
        # Handle Gemini errors — return honest fallback
        # ------------------------------------------------------------------
        if isinstance(response, dict) and response.get("error"):
            error_type = response.get("error_type", "unknown")
            print(f"[reason_generator] Gemini error ({error_type}) — using fallback reasons.")
            fallback = (
                _FALLBACK_REASONS_FAKE
                if prediction != "Real Job"
                else _FALLBACK_REASONS_REAL
            )
            return {
                "risk_score":     70 if prediction != "Real Job" else 25,
                "risk_level":     "High" if prediction != "Real Job" else "Low",
                "reasons":        fallback,
                "ai_unavailable": True,
                "ai_error_msg":   get_friendly_error_message(error_type)
            }

        if not response or (isinstance(response, str) and response.startswith("Error:")):
            fallback = (
                _FALLBACK_REASONS_FAKE
                if prediction != "Real Job"
                else _FALLBACK_REASONS_REAL
            )
            return {
                "risk_score":     70 if prediction != "Real Job" else 25,
                "risk_level":     "High" if prediction != "Real Job" else "Low",
                "reasons":        fallback,
                "ai_unavailable": True,
                "ai_error_msg":   "AI analysis temporarily unavailable."
            }

        # ------------------------------------------------------------------
        # Parse JSON response
        # ------------------------------------------------------------------
        clean = response.strip()
        if clean.startswith("```json"):
            clean = clean.replace("```json", "").replace("```", "").strip()
        elif clean.startswith("```"):
            clean = clean.replace("```", "").strip()

        data = json.loads(clean)

        risk_score = data.get("risk_score", 50)
        risk_score = max(0, min(100, risk_score))

        if risk_score <= 30:
            risk_level = "Low"
        elif risk_score <= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "risk_score":     risk_score,
            "risk_level":     risk_level,
            "reasons":        data.get("reasons", ["Unable to generate detailed analysis"]),
            "ai_unavailable": False
        }

    except Exception as e:
        print(f"[reason_generator] Unexpected error: {e}")
        fallback = (
            _FALLBACK_REASONS_FAKE
            if prediction != "Real Job"
            else _FALLBACK_REASONS_REAL
        )
        return {
            "risk_score":     50,
            "risk_level":     "Medium",
            "reasons":        fallback,
            "ai_unavailable": True,
            "ai_error_msg":   "AI analysis encountered an unexpected error."
        }