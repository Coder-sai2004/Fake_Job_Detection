# services/social_media_analyzer.py
import json
from services.gemini_service import ask_gemini


def analyze_social_presence(company_name):

    prompt = f"""
You are a Social Media Legitimacy Analyzer.

Company Name:
{company_name}

Estimate the company's social media legitimacy based on:
- LinkedIn presence
- Reddit reputation
- Overall online presence

Scoring:

90-100 = Highly Legitimate
70-89 = Likely Legitimate
50-69 = Moderate Risk
30-49 = Suspicious
0-29 = High Scam Risk

Return ONLY valid JSON in this exact format:

{{
    "overall_score": 75,
    "interpretation": "Likely Legitimate"
}}

Do not include explanations.
Do not include analysis.
Do not include markdown.
Return JSON only.
"""

    response = ask_gemini(prompt)

    try:
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()
    
        return json.loads(response)
    
    except Exception:
        return {
            "overall_score": 0,
            "interpretation": "Unavailable"
        }