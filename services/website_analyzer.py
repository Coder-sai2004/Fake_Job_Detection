# services/website_analyzer.py
#
# Scrapes a company website and uses Gemini to evaluate job legitimacy.
# Handles scraping failures and Gemini errors gracefully.

import json
from services.gemini_service import ask_gemini, get_friendly_error_message
from services.website_scraper import extract_website_content


def analyze_website(url: str) -> dict:
    """
    Scrape website and use Gemini to evaluate legitimacy.

    Returns:
    {
        "status":   "success" | "error",
        "analysis": dict | None,
        "message":  str (on error)
    }
    """

    website_data = extract_website_content(url)

    if website_data["status"] == "error":
        return {
            "status":  "error",
            "message": website_data.get("message", "Failed to fetch website"),
            "analysis": {
                "job_legitimacy_score": 50,
                "risk_level":           "Medium",
                "job_legitimacy":       False,
                "summary":              f"Website could not be fetched: {website_data.get('message', 'Unknown error')}",
                "scrape_failed":        True
            }
        }

    title   = website_data["title"]
    content = website_data["content"]

    prompt = f"""
You are an expert job fraud investigator.

Your task is NOT to determine whether the website is perfectly legitimate.

Your task is to determine whether the website provides evidence that job
opportunities associated with this company are likely genuine and trustworthy.

IMPORTANT:
The extracted website content may be incomplete because it was scraped automatically.

Do NOT heavily penalize:
- Missing contact information
- Missing pages
- Missing company details
- Incomplete content
- Lack of visible careers pages

Only evaluate what is actually present.

Website Title:
{title}

Website Content:
{content}

Analyze the website specifically for job legitimacy indicators.

Positive indicators:
- Clear company identity
- Real products or services
- Professional branding
- Business information
- Evidence of ongoing operations
- Company news or updates
- Industry-specific content
- Established business presence

Negative indicators:
- Unrealistic claims
- Get-rich-quick language
- Requests for money
- Requests for sensitive information
- Vague company identity
- No clear business purpose
- Generic placeholder content
- Suspicious recruitment language
- Contradictory information

Scoring Guidelines:
90-100: Strong evidence of a real company with legitimate operations.
70-89:  Likely legitimate company with some missing information.
40-69:  Insufficient evidence to confidently verify job legitimacy.
0-39:   Multiple indicators commonly associated with scams or fraudulent operations.

Return ONLY raw JSON — no markdown, no explanation:

{{
    "job_legitimacy_score": 0,
    "risk_level": "Low",
    "job_legitimacy": true,
    "summary": ""
}}
"""

    try:
        response = ask_gemini(prompt)

        # ------------------------------------------------------------------
        # Handle Gemini errors
        # ------------------------------------------------------------------
        if isinstance(response, dict) and response.get("error"):
            error_type = response.get("error_type", "unknown")
            print(f"[website_analyzer] Gemini error ({error_type})")
            return {
                "status": "success",
                "analysis": {
                    "job_legitimacy_score": 50,
                    "risk_level":           "Medium",
                    "job_legitimacy":       False,
                    "summary":              f"Website was fetched but AI analysis is temporarily unavailable ({get_friendly_error_message(error_type)}).",
                    "ai_unavailable":       True
                }
            }

        if not response or (isinstance(response, str) and response.startswith("Error:")):
            return {
                "status": "success",
                "analysis": {
                    "job_legitimacy_score": 50,
                    "risk_level":           "Medium",
                    "job_legitimacy":       False,
                    "summary":              "Website was fetched but AI analysis is temporarily unavailable.",
                    "ai_unavailable":       True
                }
            }

        # ------------------------------------------------------------------
        # Parse JSON
        # ------------------------------------------------------------------
        clean = response.strip()
        if clean.startswith("```json"):
            clean = clean.replace("```json", "", 1)
        if clean.startswith("```"):
            clean = clean.replace("```", "", 1)
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()

        try:
            analysis = json.loads(clean)
            return {
                "status":   "success",
                "analysis": analysis
            }

        except Exception as parse_err:
            print(f"[website_analyzer] JSON parse error: {parse_err}")
            return {
                "status": "success",
                "analysis": {
                    "job_legitimacy_score": 50,
                    "risk_level":           "Medium",
                    "job_legitimacy":       False,
                    "summary":              "Website was analyzed but response could not be parsed.",
                    "ai_unavailable":       True
                }
            }

    except Exception as e:
        print(f"[website_analyzer] Unexpected error: {e}")
        return {
            "status":  "error",
            "message": str(e),
            "analysis": {
                "job_legitimacy_score": 50,
                "risk_level":           "Medium",
                "job_legitimacy":       False,
                "summary":              "Website analysis encountered an unexpected error.",
                "ai_unavailable":       True
            }
        }