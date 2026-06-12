import json

from services.gemini_service import ask_gemini
from services.website_scraper import extract_website_content


def analyze_website(url):
    """
    Scrape website and ask Gemini
    to evaluate legitimacy.
    """

    website_data = extract_website_content(url)

    if website_data["status"] == "error":
        return website_data

    title = website_data["title"]
    content = website_data["content"]

    prompt = f"""
You are an expert job fraud investigator.

Your task is NOT to determine whether the website is perfectly legitimate.

Your task is to determine whether the website provides evidence that job opportunities associated with this company are likely genuine and trustworthy.

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

90-100:
Strong evidence of a real company with legitimate operations.

70-89:
Likely legitimate company with some missing information.

40-69:
Insufficient evidence to confidently verify job legitimacy.

0-39:
Multiple indicators commonly associated with scams or fraudulent operations.

Return ONLY raw JSON.

{{
    "job_legitimacy_score": 0,
    "risk_level": "Low | Medium | High",
    "job_legitimacy": true,
    "summary": "",
}}
"""

    try:
        response = ask_gemini(prompt)

        # Clean Gemini response
        response = response.strip()

        if response.startswith("```json"):
            response = response.replace("```json", "", 1)

        if response.startswith("```"):
            response = response.replace("```", "", 1)

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            analysis = json.loads(response)

            return {
                "status": "success",
                "analysis": analysis
            }

        except Exception as e:
            return {
                "status": "success",
                "analysis": {
                    "parse_error": str(e),
                    "raw_response": response
                }
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }