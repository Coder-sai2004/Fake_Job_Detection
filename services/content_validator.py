# services/content_validator.py
#
# Validates whether job posting content is genuine using Gemini AI.
# Handles Gemini errors gracefully — if AI is unavailable, the analysis
# proceeds with ML-only mode rather than failing the whole request.

import json
from services.gemini_service import ask_gemini, get_friendly_error_message


VALIDATION_PROMPT = """
You are a job posting validator.

Analyze the content and classify it into ONE category:

1. valid_job_description
2. code_snippet
3. random_text
4. empty_content

Rules:

- valid_job_description:
  Must clearly describe a job opening, responsibilities,
  qualifications, skills, salary, benefits, company information,
  or hiring requirements.

- code_snippet:
  Any programming code including HTML, CSS, JavaScript,
  Python, Java, SQL, C++, etc.

- random_text:
  Gibberish, meaningless text, repeated characters,
  keyboard smashing.

- empty_content:
  Empty or nearly empty text.



IMPORTANT:
Analyze the following job posting and based on real/fake job,
give the risk score based on legitimacy of the job posting.
Higher risk score means more likely to be a fake job posting.
Lower risk score means more likely to be a real job posting.


Return the answer in JSON format with the following structure:

For valid_job_description:
{
    "is_valid": true,
    "content_type": "valid_job_description",
    "reason": "...",
    "risk_score": 0
}

- risk_score must be between 0 and 100

For ALL other categories return:
{
    "is_valid": false,
    "content_type": "<category>",
    "reason": "..."
}

Return ONLY JSON.
"""


def basic_validation(text: str) -> tuple[bool, str | None]:
    if not text:
        return False, "empty_content"
    if len(text.strip()) < 20:
        return False, "too_short"
    return True, None


def validate_content(text: str) -> dict:
    """
    Validate job posting content using Gemini AI.

    Returns:
    {
        "is_valid":         bool,
        "content_type":     str,
        "risk_score":       int (0–100, only when is_valid=True),
        "risk_level":       str ("Low" | "Medium" | "High"),
        "ai_unavailable":   bool (True if Gemini failed)
    }
    """
    prompt = f"""
{VALIDATION_PROMPT}

Content:
{text}
"""

    print("Starting content validation...")
    response = ask_gemini(prompt)
    print("Gemini Response:", response)

    # ------------------------------------------------------------------
    # Handle Gemini errors — return "valid with ai_unavailable=True"
    # so the analysis can proceed in ML-only mode
    # ------------------------------------------------------------------
    if isinstance(response, dict) and response.get("error"):
        error_type = response.get("error_type", "unknown")
        print(f"[content_validator] Gemini error ({error_type}) — continuing in ML-only mode.")
        return {
            "is_valid":       True,
            "content_type":   "valid_job_description",
            "risk_score":     50,          # neutral; ML will provide the main signal
            "risk_level":     "Medium",
            "ai_unavailable": True,
            "ai_error_type":  error_type,
            "ai_error_msg":   get_friendly_error_message(error_type)
        }

    if not response or (isinstance(response, str) and response.startswith("Error:")):
        return {
            "is_valid":       True,
            "content_type":   "valid_job_description",
            "risk_score":     50,
            "risk_level":     "Medium",
            "ai_unavailable": True,
            "ai_error_type":  "unknown",
            "ai_error_msg":   "AI verification is temporarily unavailable."
        }

    # ------------------------------------------------------------------
    # Parse valid JSON response
    # ------------------------------------------------------------------
    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)

        if result.get("is_valid"):
            risk_score = result.get("risk_score", 50)
            risk_score = max(0, min(100, int(risk_score)))
            result["risk_score"] = risk_score

            if risk_score <= 30:
                result["risk_level"] = "Low"
            elif risk_score <= 60:
                result["risk_level"] = "Medium"
            else:
                result["risk_level"] = "High"

        result["ai_unavailable"] = False
        return result

    except Exception as e:
        print(f"[content_validator] JSON parse error: {e}")
        return {
            "is_valid":       True,
            "content_type":   "valid_job_description",
            "risk_score":     50,
            "risk_level":     "Medium",
            "ai_unavailable": True,
            "ai_error_type":  "invalid_response",
            "ai_error_msg":   "AI returned an unexpected response format."
        }