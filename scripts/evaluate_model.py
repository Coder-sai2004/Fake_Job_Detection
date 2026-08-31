# scripts/evaluate_model.py
#
# Evaluates the production ML model (models/job_fraud_model.pkl) on the
# cleaned dataset (data/jobs.csv) and saves real metrics to
# models/model_metrics.json.
#
# Run once (from project root):
#   python scripts/evaluate_model.py
#
# The metrics are then served by /api/model-metrics in app.py.

import sys
import os
import json
import warnings
warnings.filterwarnings("ignore")

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import joblib
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ==========================================================
# Configuration
# ==========================================================

MODEL_PATH      = "models/job_fraud_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"
DATA_PATH       = "data/jobs.csv"
CLEAN_DATA_PATH = "data/processed_jobs.csv"   # preferred if exists
OUTPUT_PATH     = "models/model_metrics.json"

TEST_SIZE   = 0.20
RANDOM_SEED = 42

# Text columns to combine (same as training notebook).
# If processed_jobs.csv already has a combined column, that takes priority.
PREFERRED_COMBINED_COLS = ["clean_text", "text"]   # checked in order
RAW_TEXT_COLUMNS = [
    "title",
    "description",
    "requirements",
    "company_profile",
    "benefits"
]


def load_data() -> pd.DataFrame:
    """Load dataset, prefer processed version if available."""
    path = CLEAN_DATA_PATH if os.path.exists(CLEAN_DATA_PATH) else DATA_PATH

    print(f"Loading dataset from: {path}")
    df = pd.read_csv(path)
    print(f"  Rows: {len(df):,}")
    return df


def prepare_features(df: pd.DataFrame) -> pd.Series:
    """
    Return the text feature column for vectorization.
    Priority: pre-combined columns (clean_text / text) > combining raw columns.
    """
    # Check for pre-combined columns first
    for col in PREFERRED_COMBINED_COLS:
        if col in df.columns:
            print(f"  Using pre-combined column: '{col}'")
            return df[col].fillna("")

    # Fall back to combining raw text columns
    available_cols = [c for c in RAW_TEXT_COLUMNS if c in df.columns]
    if not available_cols:
        raise ValueError(
            f"No usable text columns found. Expected one of {PREFERRED_COMBINED_COLS} "
            f"or raw columns {RAW_TEXT_COLUMNS}."
        )
    print(f"  Combining raw text columns: {available_cols}")
    return df[available_cols].fillna("").agg(" ".join, axis=1)


def main():
    print("=" * 60)
    print("ShieldJob AI — ML Model Evaluation")
    print("=" * 60)

    # ----------------------------------------------------------
    # 1. Load model and vectorizer
    # ----------------------------------------------------------
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at {MODEL_PATH}")
        sys.exit(1)

    if not os.path.exists(VECTORIZER_PATH):
        print(f"ERROR: Vectorizer not found at {VECTORIZER_PATH}")
        sys.exit(1)

    print("\nLoading model and vectorizer...")
    model      = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    model_name = type(model).__name__
    print(f"  Model type: {model_name}")

    # ----------------------------------------------------------
    # 2. Load dataset
    # ----------------------------------------------------------
    print("\nLoading dataset...")
    df = load_data()

    if "fraudulent" not in df.columns:
        print("ERROR: 'fraudulent' target column not found in dataset.")
        sys.exit(1)

    df = df.dropna(subset=["fraudulent"])
    y  = df["fraudulent"].astype(int)

    print(f"  Total samples:  {len(df):,}")
    print(f"  Fraudulent:     {y.sum():,}")
    print(f"  Legitimate:     {(y == 0).sum():,}")
    print(f"  Fraud rate:     {y.mean()*100:.1f}%")

    # ----------------------------------------------------------
    # 3. Prepare features
    # ----------------------------------------------------------
    print("\nPreparing text features...")
    X_text = prepare_features(df)

    # ----------------------------------------------------------
    # 4. Train/test split (use SAME seed as training if known)
    # ----------------------------------------------------------
    print(f"\nSplitting data (test={TEST_SIZE*100:.0f}%, seed={RANDOM_SEED})...")
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        X_text, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=y
    )
    print(f"  Train samples: {len(X_train_text):,}")
    print(f"  Test samples:  {len(X_test_text):,}")

    # ----------------------------------------------------------
    # 5. Vectorize (transform only — never refit)
    # ----------------------------------------------------------
    print("\nVectorizing test set...")
    X_test_vec = vectorizer.transform(X_test_text)

    # ----------------------------------------------------------
    # 6. Predict
    # ----------------------------------------------------------
    print("Running predictions...")
    y_pred      = model.predict(X_test_vec)
    y_pred_prob = model.predict_proba(X_test_vec)[:, 1]

    # ----------------------------------------------------------
    # 7. Compute metrics
    # ----------------------------------------------------------
    print("\nComputing metrics...")
    accuracy  = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall    = recall_score(y_test, y_pred, zero_division=0)
    f1        = f1_score(y_test, y_pred, zero_division=0)
    roc_auc   = roc_auc_score(y_test, y_pred_prob)
    cm        = confusion_matrix(y_test, y_pred)

    tn, fp, fn, tp = cm.ravel()

    print(f"\n  Accuracy:  {accuracy*100:.2f}%")
    print(f"  Precision: {precision*100:.2f}%")
    print(f"  Recall:    {recall*100:.2f}%")
    print(f"  F1 Score:  {f1*100:.2f}%")
    print(f"  ROC-AUC:   {roc_auc*100:.2f}%")
    print(f"\n  Confusion Matrix:")
    print(f"    True Negatives:  {tn}  (Real jobs correctly identified)")
    print(f"    False Positives: {fp}  (Real jobs flagged as fake)")
    print(f"    False Negatives: {fn}  (Fake jobs missed)")
    print(f"    True Positives:  {tp}  (Fake jobs correctly caught)")

    # ----------------------------------------------------------
    # 8. Build output dict
    # ----------------------------------------------------------
    metrics = {
        "model_info": {
            "name":       model_name,
            "file":       MODEL_PATH,
            "vectorizer": VECTORIZER_PATH,
        },
        "dataset_info": {
            "total_samples":     int(len(df)),
            "legitimate_jobs":   int((y == 0).sum()),
            "fraudulent_jobs":   int(y.sum()),
            "fraud_rate_pct":    round(float(y.mean()) * 100, 2),
            "test_size_pct":     int(TEST_SIZE * 100),
            "test_samples":      int(len(X_test_text)),
        },
        "metrics": {
            "accuracy":  round(float(accuracy)  * 100, 2),
            "precision": round(float(precision) * 100, 2),
            "recall":    round(float(recall)    * 100, 2),
            "f1_score":  round(float(f1)        * 100, 2),
            "roc_auc":   round(float(roc_auc)   * 100, 2),
        },
        "confusion_matrix": {
            "true_negatives":   int(tn),
            "false_positives":  int(fp),
            "false_negatives":  int(fn),
            "true_positives":   int(tp),
        },
        "computed_at": datetime.now().isoformat(),
    }

    # ----------------------------------------------------------
    # 9. Save to JSON
    # ----------------------------------------------------------
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nDone! Metrics saved to: {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()
