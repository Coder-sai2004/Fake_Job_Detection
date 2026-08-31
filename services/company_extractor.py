# services/company_extractor.py
#
# Extracts the company name from a job description using a layered approach:
#
#   Layer 1 — Explicit field patterns (regex):
#     Looks for "Company: X", "Employer: X", "Organization: X", etc.
#     These are the most reliable signals.
#
#   Layer 2 — Contextual NLP heuristics:
#     Looks for patterns like "at [Company]", "hiring at [Company]",
#     "join [Company]", "About [Company]".
#     Uses capitalization heuristics to validate extracted names.
#
#   Layer 3 — Gemini AI fallback:
#     Only used if Layers 1 and 2 both fail.
#     The result is tagged as "ai_fallback" so callers can apply
#     appropriate skepticism.
#
# Returns:
#   {
#     "company":  str | None,
#     "source":   "regex_field" | "regex_context" | "ai_fallback" | "not_found",
#     "confidence": "high" | "medium" | "low"
#   }

import re
import json
from services.gemini_service import ask_gemini


# -----------------------------------------------------------------------
# Layer 1 — Explicit labelled field patterns
# -----------------------------------------------------------------------

_FIELD_PATTERNS = [
    r"(?:Company|Employer|Organization|Firm|Recruiter|Client)[\s]*:[\s]*(.+)",
    r"(?:Hiring|Posted by|Sourced by)[\s]*:[\s]*(.+)",
    r"(?:About|About Us|About the Company)[\s]*:[\s]*(.+)",
]


def _extract_via_field_patterns(text: str) -> str | None:
    for pattern in _FIELD_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            candidate = candidate.split("\n")[0].strip()   # first line only
            candidate = re.sub(r"[|•\-–—]+$", "", candidate).strip()
            if 2 <= len(candidate) <= 80:
                return candidate
    return None


# -----------------------------------------------------------------------
# Layer 2 — Contextual heuristic patterns
# -----------------------------------------------------------------------

_CONTEXT_PATTERNS = [
    r"(?:join|joining|at|with|for)\s+([A-Z][A-Za-z0-9\s&\.\-]{2,40}?)(?:\s+(?:is|as|are|for|to|and|in|\.|,))",
    r"([A-Z][A-Za-z0-9\s&\.\-]{2,40}?)\s+(?:is|are)\s+(?:hiring|looking|seeking|recruiting)",
    r"(?:work(?:ing)?\s+at|employed\s+at)\s+([A-Z][A-Za-z0-9\s&\.\-]{2,40}?)(?:\s|\.|,)",
]

_VALID_COMPANY_WORDS = {
    "inc", "corp", "ltd", "llc", "plc", "group",
    "technologies", "tech", "solutions", "services",
    "systems", "consulting", "global", "international",
    "enterprise", "bank", "capital"
}


def _looks_like_company(name: str) -> bool:
    """Basic sanity check on an extracted candidate name."""
    if not name or len(name) < 3:
        return False
    words = name.lower().split()
    # Must have at least one capital word OR a known company suffix
    has_proper_noun = any(w[0].isupper() for w in name.split() if w)
    has_company_word = any(w in _VALID_COMPANY_WORDS for w in words)
    return has_proper_noun or has_company_word


def _extract_via_context(text: str) -> str | None:
    for pattern in _CONTEXT_PATTERNS:
        for match in re.finditer(pattern, text):
            candidate = match.group(1).strip()
            candidate = re.sub(r"\s+", " ", candidate)
            if _looks_like_company(candidate):
                return candidate
    return None


# -----------------------------------------------------------------------
# Layer 3 — Gemini AI fallback
# -----------------------------------------------------------------------

def _extract_via_gemini(text: str) -> str | None:
    # Limit text sent to Gemini to avoid large prompts
    excerpt = text[:1500]

    prompt = f"""
Extract the hiring company name from this job posting.

Rules:
- Return ONLY the company name as plain text.
- No explanation, no punctuation, no JSON, no markdown.
- If no company name can be identified, return exactly: UNKNOWN

Job Posting:
{excerpt}
"""
    try:
        response = ask_gemini(prompt)

        # Handle error dict from updated gemini_service
        if isinstance(response, dict) and response.get("error"):
            return None

        if not response or response.startswith("Error:"):
            return None

        name = response.strip().strip('"').strip("'")
        if name.upper() == "UNKNOWN" or not name:
            return None

        # Quick sanity check
        if len(name) > 100 or "\n" in name:
            return None

        return name

    except Exception:
        return None


# -----------------------------------------------------------------------
# Public API
# -----------------------------------------------------------------------

def extract_company_name(job_description: str) -> str | None:
    """
    Extract the company name from a job description.
    Returns the company name string or None.
    Kept simple for backward compatibility with existing callers.
    """
    result = extract_company_name_with_metadata(job_description)
    return result["company"]


def extract_company_name_with_metadata(job_description: str) -> dict:
    """
    Extract company name with provenance metadata.

    Returns:
    {
        "company":    str | None,
        "source":     "regex_field" | "regex_context" | "ai_fallback" | "not_found",
        "confidence": "high" | "medium" | "low"
    }
    """
    if not job_description:
        return {"company": None, "source": "not_found", "confidence": "low"}

    # Layer 1
    company = _extract_via_field_patterns(job_description)
    if company:
        return {"company": company, "source": "regex_field", "confidence": "high"}

    # Layer 2
    company = _extract_via_context(job_description)
    if company:
        return {"company": company, "source": "regex_context", "confidence": "medium"}

    # Layer 3
    company = _extract_via_gemini(job_description)
    if company:
        return {"company": company, "source": "ai_fallback", "confidence": "low"}

    return {"company": None, "source": "not_found", "confidence": "low"}