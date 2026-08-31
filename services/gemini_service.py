# services/gemini_service.py
#
# Centralized Gemini API client with structured error handling.
#
# ask_gemini() returns:
#   - str: the response text on success
#   - dict: {"error": True, "error_type": str, "message": str} on failure
#
# Callers check: if isinstance(response, dict) and response.get("error")

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("GEMINI_API_KEY", "")

if _API_KEY:
    genai.configure(api_key=_API_KEY)

_model = None


def _get_model():
    """Lazy-load the Gemini model to avoid init errors if key is missing."""
    global _model
    if _model is None:
        _model = genai.GenerativeModel("models/gemini-2.5-flash")
    return _model


def ask_gemini(prompt: str) -> str | dict:
    """
    Send a prompt to Gemini and return the response text.

    On success: returns str (the model's response)
    On failure: returns dict with keys:
        {
            "error":      True,
            "error_type": "api_key" | "quota" | "timeout" | "network" | "invalid_response" | "unknown",
            "message":    str  (safe to log, do NOT expose to frontend)
        }
    """

    if not _API_KEY:
        return {
            "error":      True,
            "error_type": "api_key",
            "message":    "GEMINI_API_KEY not configured in environment."
        }

    try:
        model    = _get_model()
        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            return {
                "error":      True,
                "error_type": "invalid_response",
                "message":    "Gemini returned an empty or unexpected response structure."
            }

        return response.text

    except Exception as e:
        error_str = str(e).lower()

        if "quota" in error_str or "429" in error_str or "resource_exhausted" in error_str:
            error_type = "quota"
        elif "timeout" in error_str or "deadline" in error_str:
            error_type = "timeout"
        elif "connection" in error_str or "network" in error_str:
            error_type = "network"
        elif "api_key" in error_str or "invalid_api" in error_str or "permission" in error_str:
            error_type = "api_key"
        else:
            error_type = "unknown"

        print(f"[gemini_service] Error ({error_type}): {e}")

        return {
            "error":      True,
            "error_type": error_type,
            "message":    str(e)
        }


def get_friendly_error_message(error_type: str) -> str:
    """Return a user-friendly (non-sensitive) error message for the frontend."""
    messages = {
        "api_key": "AI service is not configured. Please check your API key.",
        "quota":   "AI service quota has been reached. Please try again later.",
        "timeout": "AI service timed out. Please try again.",
        "network": "Unable to reach AI service. Please check your connection.",
        "invalid_response": "AI service returned an unexpected response.",
        "unknown": "AI verification is temporarily unavailable.",
    }
    return messages.get(error_type, "AI verification is temporarily unavailable.")