from flask import Flask, render_template, request, jsonify
import joblib
import json
import os

from services.gemini_service import ask_gemini, get_friendly_error_message
from services.content_validator import (
    validate_content,
    basic_validation
)
from services.reason_generator import generate_job_analysis
from services.website_analyzer import analyze_website
from services.company_extractor import extract_company_name
from services.social_media_analyzer import analyze_social_presence

app = Flask(__name__)

ENABLE_AI_VALIDATION = True

# Load ML assets
model     = joblib.load("models/job_fraud_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


# ==========================================================
# Helper Functions
# ==========================================================

def run_ml_prediction(job_description: str) -> dict:
    job_vector   = vectorizer.transform([job_description])
    prediction   = model.predict(job_vector)
    probabilities = model.predict_proba(job_vector)[0]

    print("Prediction Raw:", prediction)
    print("Prediction Probabilities:", probabilities)

    real_probability = probabilities[0] * 100
    fake_probability = probabilities[1] * 100

    prediction_text = (
        "Real Job"
        if prediction[0] == 0
        else "Fake Job"
    )

    ml_score = real_probability  # higher = more legitimate

    return {
        "prediction":       prediction_text,
        "real_probability": round(real_probability, 2),
        "fake_probability": round(fake_probability, 2),
        "ml_score":         round(ml_score, 2)
    }


def run_website_analysis(company_website: str) -> dict | None:
    if not company_website:
        return None

    website_result = analyze_website(company_website)

    # Always return analysis object if present (even on "error" status,
    # website_analyzer now provides a safe fallback analysis)
    return website_result.get("analysis", None)


def run_social_analysis(job_description: str) -> dict | None:
    company_name = extract_company_name(job_description)

    if not company_name:
        return None

    return analyze_social_presence(company_name)


def calculate_final_score(
    ml_score: float,
    ai_score: float,
    website_score: float,
    social_score: float
) -> dict:
    final_score = (
        ml_score      * 0.30 +
        ai_score      * 0.30 +
        website_score * 0.20 +
        social_score  * 0.20
    )

    if final_score >= 70:
        final_prediction = "Real Job"
    elif final_score >= 50:
        final_prediction = "Suspicious Job"
    else:
        final_prediction = "Fake Job"

    return {
        "final_score":      round(final_score, 2),
        "final_prediction": final_prediction
    }


# ==========================================================
# Routes
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    prediction_text  = ""
    job_description  = ""
    ai_unavailable   = False
    ai_error_message = ""

    analysis = {
        "risk_score": None,
        "risk_level": None,
        "reasons":    []
    }

    ml_result        = None
    website_analysis = None
    social_analysis  = None

    ai_score      = 50
    ml_score      = 50
    website_score = 50
    social_score  = 50
    final_result  = None

    if request.method == "POST":

        job_description = request.form.get("job_description", "")
        company_website = request.form.get("company_website", "").strip()

        # --------------------------------------------------
        # Basic Validation
        # --------------------------------------------------
        valid, error = basic_validation(job_description)

        if not valid:
            prediction_text = f"Invalid Input: {error}"

        else:

            # ----------------------------------------------
            # AI Validation (Gemini content check)
            # ----------------------------------------------
            validation_result = {"is_valid": True}

            if ENABLE_AI_VALIDATION:
                validation_result = validate_content(job_description)

                content_risk_score = validation_result.get("risk_score", 50)
                ai_score           = 100 - content_risk_score

                # Propagate AI unavailability flag
                if validation_result.get("ai_unavailable"):
                    ai_unavailable   = True
                    ai_error_message = validation_result.get(
                        "ai_error_msg",
                        "AI verification is temporarily unavailable."
                    )

                print("Validation Result:", validation_result)
                print(f"Content Risk Score: {content_risk_score}")

            if not validation_result.get("is_valid", False):
                prediction_text = (
                    f"Invalid Input: {validation_result.get('content_type', 'unknown')}"
                )

            else:

                # ------------------------------------------
                # ML Prediction (always runs)
                # ------------------------------------------
                ml_result       = run_ml_prediction(job_description)
                prediction_text = ml_result["prediction"]
                ml_score        = ml_result["ml_score"]

                # ------------------------------------------
                # Website Analysis
                # ------------------------------------------
                website_analysis = run_website_analysis(company_website)
                website_score    = (
                    website_analysis.get("job_legitimacy_score", 50)
                    if website_analysis
                    else 50
                )

                # ------------------------------------------
                # Social Media Analysis (real search)
                # ------------------------------------------
                social_analysis = run_social_analysis(job_description)
                social_score    = (
                    social_analysis["overall_score"]
                    if social_analysis
                    else 50
                )

                # ------------------------------------------
                # Reason Generation
                # ------------------------------------------
                analysis = generate_job_analysis(job_description, prediction_text)

                # Merge AI unavailability from reason generator
                if analysis.get("ai_unavailable"):
                    ai_unavailable = True
                    ai_error_message = analysis.get(
                        "ai_error_msg",
                        "AI verification is temporarily unavailable."
                    )

                # ------------------------------------------
                # Final Score Calculation
                # ------------------------------------------
                final_result = calculate_final_score(
                    ml_score,
                    ai_score,
                    website_score,
                    social_score
                )

    return render_template(
        "index.html",

        # Final Result
        prediction=(
            final_result["final_prediction"]
            if final_result else ""
        ),
        final_score=(
            final_result["final_score"]
            if final_result else None
        ),

        # Job Info
        job_description=job_description,

        # Component Scores
        ml_score=ml_score,
        ai_score=ai_score,
        website_score=website_score,
        social_score=social_score,

        # AI Analysis
        risk_level=analysis["risk_level"],
        reasons=analysis["reasons"],

        # Detailed Analysis Objects
        website_analysis=website_analysis,
        social_analysis=social_analysis,

        # AI Status Flags
        ai_unavailable=ai_unavailable,
        ai_error_message=ai_error_message,
    )


@app.route("/api/model-metrics")
def model_metrics():
    """
    Return ML model performance metrics from the pre-computed metrics file.
    The metrics file is generated by running: python scripts/evaluate_model.py
    """
    metrics_path = "models/model_metrics.json"

    if not os.path.exists(metrics_path):
        return jsonify({
            "status": "not_computed",
            "message": (
                "Model metrics have not been computed yet. "
                "Run 'python scripts/evaluate_model.py' to generate them."
            )
        }), 404

    try:
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
        return jsonify({"status": "ok", "metrics": metrics})
    except Exception as e:
        print(f"[model_metrics] Error reading metrics: {e}")
        return jsonify({"status": "error", "message": "Could not read metrics file."}), 500


@app.route("/test-gemini")
def test_gemini():
    prompt = "Explain what a fake job posting is in 3 lines."
    response = ask_gemini(prompt)

    if isinstance(response, dict) and response.get("error"):
        return jsonify({
            "status": "error",
            "error_type": response.get("error_type"),
            "message":    get_friendly_error_message(response.get("error_type", "unknown"))
        }), 503

    return jsonify({"status": "success", "response": response})


if __name__ == "__main__":
    app.run(debug=True)