import json
from services.gemini_service import ask_gemini


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
Analyze the following job posting and based on real//fake job,and give the risk score based on legitimity of the job posting.
Higher risk score means more likely to be a fake job posting.
Lower risk score means more likely to be a real job posting.


return the answer in json format with the following structure:
Return:

{
    "is_valid": true,
    "content_type": "valid_job_description",
    "reason": "...",
    "risk_score": 0,
}
For valid_job_description:

- risk_score must be between 0 and 100


ONLY when the content is a valid job description.

For ALL other categories return:

{
    "is_valid": false,
    "content_type": "<category>",
    "reason": "..."
}

Return ONLY JSON.
"""


def basic_validation(text):

    if not text:
        return False, "empty_content"

    if len(text.strip()) < 20:
        return False, "too_short"

    return True, None


def validate_content(text):

    prompt = f"""
{VALIDATION_PROMPT}

Content:
{text}
"""
    print("Starting validation...")


    response = ask_gemini(prompt)

    print("Gemini Response:")
    print(response)
    # Gemini/API Error
    if response.startswith("Error:"):
        return {
            "is_valid": False,
            "content_type": "system_error",
            "reason": response
        }

    try:

        # Remove markdown wrappers if Gemini returns them
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        result = json.loads(response)
        
        if result.get("is_valid"):
        
            risk_score = result.get("risk_score", 50)
        
            risk_score = max(
                0,
                min(
                    100,
                    int(risk_score)
                )
            )
        
            result["risk_score"] = risk_score
        
            if risk_score <= 30:
                result["risk_level"] = "Low"
        
            elif risk_score <= 60:
                result["risk_level"] = "Medium"
        
            else:
                result["risk_level"] = "High"
        
        return result

    except Exception:

        return {
            "is_valid": False,
            "content_type": "unknown",
            "reason": "Invalid AI response"
        }