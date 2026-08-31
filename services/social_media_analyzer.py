# services/social_media_analyzer.py
#
# Company social media & reputation verifier.
#
# Two modes (auto-selected):
#
#   Mode 1 — REAL SEARCH (when a search provider is configured):
#     Runs actual Google CSE / Brave API queries and inspects real URLs.
#     Gemini only summarizes the collected evidence.
#
#   Mode 2 — AI KNOWLEDGE CHECK (when no search provider is available):
#     Uses Gemini's training knowledge to reason about the company's
#     legitimacy. Clearly labeled as "AI Knowledge — not real-time search".
#     Much more defensible than asking "does company X have LinkedIn?"
#     because it asks Gemini to reason with confidence ratings and caveats.

import json
from services.search_service import search, is_configured, active_provider
from services.gemini_service import ask_gemini, get_friendly_error_message


# -----------------------------------------------------------------------
# Real-Search Signal Detectors
# -----------------------------------------------------------------------

_LINKEDIN_DOMAINS = ["linkedin.com/company/", "linkedin.com/in/"]
_REVIEW_DOMAINS   = ["glassdoor.com", "indeed.com", "trustpilot.com",
                     "ambitionbox.com", "comparably.com"]
_SCAM_KEYWORDS    = ["scam", "fraud", "fake", "cheating", "beware",
                     "warning", "avoid", "complaint", "blacklist"]


def _check_linkedin(results):
    for r in results:
        if any(d in r.get("url","").lower() for d in _LINKEDIN_DOMAINS):
            return {"status": "Found", "url": r["url"], "title": r["title"]}
    return {"status": "Not Found"}


def _check_reddit(results):
    found = [r for r in results if "reddit.com" in r.get("url","").lower()]
    if found:
        return {"status": "Found", "count": len(found),
                "results": [{"url": x["url"], "title": x["title"]} for x in found[:3]]}
    return {"status": "Not Found"}


def _check_reviews(results):
    found = [r for r in results if any(d in r.get("url","").lower() for d in _REVIEW_DOMAINS)]
    if found:
        return {"status": "Found", "count": len(found),
                "results": [{"url": x["url"], "title": x["title"]} for x in found[:3]]}
    return {"status": "Not Found"}


def _detect_scam_signals(results):
    signals = []
    for r in results:
        text = (r.get("title","") + " " + r.get("snippet","")).lower()
        for kw in _SCAM_KEYWORDS:
            if kw in text:
                signals.append(f'"{kw}" in: {r["title"][:60]}')
                break
    return signals


def _score_from_evidence(linkedin, reddit, reviews, scam_signals, total):
    score = 50
    if linkedin["status"] == "Found": score += 20
    if reddit["status"]   == "Found": score += 10
    if reviews["status"]  == "Found": score += 15
    if total >= 5:                     score += 5
    score -= len(scam_signals) * 15
    return max(0, min(100, score))


# -----------------------------------------------------------------------
# Mode 1: Real Search (Google CSE or Brave)
# -----------------------------------------------------------------------

def _analyze_with_real_search(company_name: str) -> dict:
    queries = [
        f'"{company_name}" company LinkedIn',
        f'"{company_name}" Reddit employees reviews',
        f'"{company_name}" glassdoor indeed reviews',
        f'"{company_name}" scam fraud complaint',
    ]

    all_results = []
    for query in queries:
        all_results.extend(search(query, num=5))

    # If search API is blocked (e.g. 403 billing/quota) and returned no results,
    # gracefully fall back to AI Knowledge Mode so the user gets a meaningful analysis
    if not all_results:
        print(f"[social_media_analyzer] Real search returned 0 results (API likely unauthenticated/403). Falling back to AI Knowledge mode.")
        return _analyze_with_gemini_knowledge(company_name)

    linkedin_ev = _check_linkedin(all_results)
    reddit_ev   = _check_reddit(all_results)
    reviews_ev  = _check_reviews(all_results)
    scam_sigs   = _detect_scam_signals(all_results)
    score       = _score_from_evidence(linkedin_ev, reddit_ev, reviews_ev,
                                        scam_sigs, len(all_results))

    label = ("Highly Legitimate" if score >= 80 else
             "Likely Legitimate" if score >= 65 else
             "Moderate Confidence" if score >= 45 else
             "Suspicious — Limited Presence" if score >= 30 else
             "High Risk — No Verifiable Presence")

    # Gemini summarizes the REAL evidence (not inventing it)
    ev_text = (
        f"Company: {company_name}\n"
        f"LinkedIn: {linkedin_ev['status']}\n"
        f"Reddit: {reddit_ev['status']}\n"
        f"Reviews: {reviews_ev['status']}\n"
        f"Scam signals: {len(scam_sigs)}\n"
        f"Search results analyzed: {len(all_results)}\n"
        f"Score: {score}/100"
    )
    ai_prompt = (
        "Summarize in 1-2 professional sentences what this REAL search evidence "
        "suggests about job legitimacy. Do not invent any information.\n\n"
        + ev_text
    )
    ai_resp = ask_gemini(ai_prompt)
    ai_summary = (
        ai_resp if isinstance(ai_resp, str) and not ai_resp.startswith("Error:")
        else f"Legitimacy score: {score}/100. Evidence collected from real web search."
    )

    seen, unique = set(), []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append({"title": r["title"], "url": r["url"]})
        if len(unique) >= 5: break

    return {
        "overall_score":  score,
        "interpretation": label,
        "ai_summary":     ai_summary,
        "evidence": {
            "linkedin":       linkedin_ev,
            "reddit":         reddit_ev,
            "reviews":        reviews_ev,
            "scam_signals":   scam_sigs[:5],
            "search_results": unique
        },
        "verification_method":  "real_search_" + active_provider(),
        "ai_summary_available": True
    }


# -----------------------------------------------------------------------
# Mode 2: AI Knowledge Check (Gemini training data, no real search)
# -----------------------------------------------------------------------

def _analyze_with_gemini_knowledge(company_name: str) -> dict:
    """
    Uses Gemini's training knowledge to reason about company legitimacy.
    Clearly labeled as AI knowledge, not real-time verified.
    Structured response with confidence ratings prevents hallucination loops.
    """

    prompt = f"""
You are a company legitimacy analyst using your training knowledge.

Company being analyzed: "{company_name}"

Answer the following questions based ONLY on what you know from your training data.
Be honest about uncertainty. Do NOT make up facts.

Return ONLY valid JSON with this exact structure:

{{
    "known_company": true or false,
    "knowledge_confidence": 0,
    "linkedin_likely": true or false,
    "has_reviews": true or false,
    "scam_reports_known": true or false,
    "company_type": "tech/finance/healthcare/unknown/etc",
    "summary": "1-2 sentence summary of what you know",
    "legitimacy_score": 0,
    "caveats": "what you're uncertain about"
}}

Rules:
- knowledge_confidence: 0-100, how confident you are in your knowledge (0 = never heard of company)
- legitimacy_score: 0-100 based on your knowledge (50 = unknown/neutral)
- If you have never heard of the company, set known_company=false and legitimacy_score=50
- Do NOT invent LinkedIn profiles or review links
- Return ONLY valid JSON, no markdown
"""

    response = ask_gemini(prompt)

    # Handle Gemini errors
    if isinstance(response, dict) and response.get("error"):
        error_type = response.get("error_type", "unknown")
        return {
            "overall_score":  50,
            "interpretation": "Unable to verify — AI service unavailable",
            "ai_summary":     get_friendly_error_message(error_type),
            "evidence": {
                "linkedin":       {"status": "Unable to Verify"},
                "reddit":         {"status": "Unable to Verify"},
                "reviews":        {"status": "Unable to Verify"},
                "scam_signals":   [],
                "search_results": []
            },
            "verification_method":  "unavailable",
            "ai_summary_available": False
        }

    # Parse response
    try:
        clean = response.strip().replace("```json","").replace("```","").strip()
        data = json.loads(clean)

        score      = max(0, min(100, int(data.get("legitimacy_score", 50))))
        confidence = data.get("knowledge_confidence", 0)
        known      = data.get("known_company", False)

        # If Gemini doesn't know the company, neutral score
        if not known or confidence < 20:
            score = 50

        label = ("Highly Legitimate" if score >= 80 else
                 "Likely Legitimate" if score >= 65 else
                 "Moderate Confidence" if score >= 45 else
                 "Suspicious — Limited Presence" if score >= 30 else
                 "High Risk — No Verifiable Presence")

        linkedin_status = "Likely Present" if data.get("linkedin_likely") else "Unknown"
        reviews_status  = "Likely Present" if data.get("has_reviews")     else "Unknown"

        summary = data.get("summary", "No specific knowledge found about this company.")
        caveats = data.get("caveats", "Based on AI training data only — not real-time verified.")

        return {
            "overall_score":  score,
            "interpretation": label,
            "ai_summary":     f"{summary} Note: {caveats}",
            "evidence": {
                "linkedin":       {"status": linkedin_status},
                "reddit":         {"status": "Unknown"},
                "reviews":        {"status": reviews_status},
                "scam_signals":   ["Scam reports known"] if data.get("scam_reports_known") else [],
                "search_results": []
            },
            "verification_method":  "ai_knowledge",
            "knowledge_confidence": confidence,
            "ai_summary_available": True
        }

    except Exception as e:
        print(f"[social_media_analyzer] Gemini parse error: {e}")
        return {
            "overall_score":  50,
            "interpretation": "Unable to parse AI response",
            "ai_summary":     "Company verification encountered an unexpected error.",
            "evidence": {
                "linkedin":       {"status": "Unknown"},
                "reddit":         {"status": "Unknown"},
                "reviews":        {"status": "Unknown"},
                "scam_signals":   [],
                "search_results": []
            },
            "verification_method":  "ai_knowledge",
            "ai_summary_available": False
        }


# -----------------------------------------------------------------------
# Public Entry Point
# -----------------------------------------------------------------------

def analyze_social_presence(company_name: str) -> dict:
    """
    Main entry point. Auto-selects the best available verification mode.

    Returns:
    {
        "overall_score":         int (0-100),
        "interpretation":        str,
        "ai_summary":            str,
        "evidence":              dict,
        "verification_method":   "real_search_brave" | "real_search_google_cse"
                                  | "ai_knowledge" | "unavailable",
        "ai_summary_available":  bool
    }
    """
    if not company_name:
        return None

    if is_configured():
        # Mode 1: Real web search
        return _analyze_with_real_search(company_name)
    else:
        # Mode 2: Gemini knowledge check (clearly labeled)
        return _analyze_with_gemini_knowledge(company_name)