# services/search_service.py
#
# Search provider service wrapper (Brave Search / Google CSE).
# Returns [] when no provider is configured, triggering AI Knowledge Mode.

import os
import requests
from dotenv import load_dotenv

load_dotenv()

_BRAVE_API_KEY   = os.getenv("BRAVE_SEARCH_API_KEY", "").strip()
_GOOGLE_API_KEY  = os.getenv("GOOGLE_CSE_API_KEY", "").strip()
_GOOGLE_CSE_ID   = os.getenv("GOOGLE_CSE_ID", "").strip()
_TIMEOUT = 8


def is_configured() -> bool:
    """Return True if any valid search provider key is configured."""
    has_brave  = bool(_BRAVE_API_KEY and not _BRAVE_API_KEY.startswith("your_"))
    has_google = bool(_GOOGLE_API_KEY and _GOOGLE_CSE_ID and not _GOOGLE_API_KEY.startswith("your_"))
    return has_brave or has_google


def active_provider() -> str:
    if _BRAVE_API_KEY and not _BRAVE_API_KEY.startswith("your_"):
        return "brave"
    if _GOOGLE_API_KEY and _GOOGLE_CSE_ID and not _GOOGLE_API_KEY.startswith("your_"):
        return "google_cse"
    return "none"


def search(query: str, num: int = 5) -> list[dict]:
    """Search using active provider. Returns [] if unconfigured or on error."""
    provider = active_provider()

    if provider == "brave":
        headers = {"Accept": "application/json", "X-Subscription-Token": _BRAVE_API_KEY}
        try:
            r = requests.get("https://api.search.brave.com/res/v1/web/search",
                             headers=headers, params={"q": query, "count": num}, timeout=_TIMEOUT)
            if r.ok:
                return [
                    {"title": x.get("title", ""), "url": x.get("url", ""), "snippet": x.get("description", "")}
                    for x in r.json().get("web", {}).get("results", [])
                ]
        except Exception as e:
            print(f"[search_service][brave] Error: {e}")

    elif provider == "google_cse":
        try:
            r = requests.get("https://www.googleapis.com/customsearch/v1", timeout=_TIMEOUT,
                             params={"key": _GOOGLE_API_KEY, "cx": _GOOGLE_CSE_ID, "q": query, "num": min(10, num)})
            if r.ok:
                return [
                    {"title": x.get("title", ""), "url": x.get("link", ""), "snippet": x.get("snippet", "")}
                    for x in r.json().get("items", [])
                ]
        except Exception as e:
            print(f"[search_service][google] Error: {e}")

    return []
