# scripts/evaluate_model.py
#
# Rigorous, leak-free 5-Fold Stratified Cross-Validation of the ShieldJob AI
# Balanced Random Forest model.
#
# Generates out-of-fold predictions and writes honest benchmark metrics to
# models/model_metrics.json.
#
# Run from project root:
#   python scripts/evaluate_model.py

import os
import sys
import json
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

DATA_PATH       = os.path.join(PROJECT_ROOT, "data", "processed_jobs.csv")
RAW_DATA_PATH   = os.path.join(PROJECT_ROOT, "data", "jobs.csv")
OUTPUT_PATH     = os.path.join(PROJECT_ROOT, "models", "model_metrics.json")
MODEL_PATH      = "models/job_fraud_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

N_SPLITS            = 5
DECISION_THRESHOLD  = 0.24   # Calibrated threshold for ~85% fraud recall on balanced RF
RANDOM_SEED         = 42
RAW_TEXT_COLUMNS    = ["title", "description", "requirements", "company_profile", "benefits"]


def load_dataset() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        print(f"Loading processed dataset: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
    else:
        print(f"Loading raw dataset: {RAW_DATA_PATH}")
        df = pd.read_csv(RAW_DATA_PATH)
    return df


def extract_text_series(df: pd.DataFrame) -> pd.Series:
    for col in ["clean_text", "text"]:
        if col in df.columns:
            return df[col].fillna("")
    
    available = [c for c in RAW_TEXT_COLUMNS if c in df.columns]
    return df[available].fillna("").agg(" ".join, axis=1)


def main():
    print("=" * 65)
    print("ShieldJob AI — Leak-Free 5-Fold Stratified Cross-Validation")
    print("=" * 65)

    df = load_dataset()
    df = df.dropna(subset=["fraudulent"])

    X_text = extract_text_series(df)
    y = df["fraudulent"].astype(int).values

    total_samples = len(df)
    fraud_count = int(y.sum())
    legit_count = int((y == 0).sum())
    fraud_rate = (fraud_count / total_samples) * 100

    print(f"\nDataset Statistics:")
    print(f"  Total Postings : {total_samples:,}")
    print(f"  Legitimate Jobs: {legit_count:,} ({100 - fraud_rate:.2f}%)")
    print(f"  Fraudulent Jobs: {fraud_count:,} ({fraud_rate:.2f}%)")
    print(f"  Baseline Accuracy (predict all real): {100 - fraud_rate:.2f}%")

    print(f"\nRunning {N_SPLITS}-Fold Stratified CV (Threshold = {DECISION_THRESHOLD})...")

    oof_probs = np.zeros(total_samples)
    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)

    for fold, (train_idx, val_idx) in enumerate(cv.split(X_text, y), start=1):
        X_train_fold = X_text.iloc[train_idx]
        y_train_fold = y[train_idx]
        X_val_fold   = X_text.iloc[val_idx]
        y_val_fold   = y[val_idx]

        # Fit TF-IDF ONLY on train fold to avoid test leakage
        vec = TfidfVectorizer(
            max_features=12000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=2
        )
        X_train_vec = vec.fit_transform(X_train_fold)
        X_val_vec   = vec.transform(X_val_fold)

        clf = RandomForestClassifier(
            n_estimators=100,
            class_weight="balanced",
            random_state=RANDOM_SEED,
            n_jobs=-1
        )
        clf.fit(X_train_vec, y_train_fold)

        probs = clf.predict_proba(X_val_vec)[:, 1]
        oof_probs[val_idx] = probs

        preds = (probs >= DECISION_THRESHOLD).astype(int)
        fold_rec = recall_score(y_val_fold, preds, zero_division=0)
        fold_prec = precision_score(y_val_fold, preds, zero_division=0)
        fold_acc = accuracy_score(y_val_fold, preds)
        print(f"  Fold {fold}/{N_SPLITS}: Acc={fold_acc*100:.2f}% | Scam Recall={fold_rec*100:.2f}% | Precision={fold_prec*100:.2f}%")

    oof_preds = (oof_probs >= DECISION_THRESHOLD).astype(int)

    acc       = accuracy_score(y, oof_preds)
    precision = precision_score(y, oof_preds, zero_division=0)
    recall    = recall_score(y, oof_preds, zero_division=0)
    f1        = f1_score(y, oof_preds, zero_division=0)
    roc_auc   = roc_auc_score(y, oof_probs)
    cm        = confusion_matrix(y, oof_preds)

    tn, fp, fn, tp = cm.ravel()

    print("\n" + "=" * 65)
    print("VERIFIED OUT-OF-FOLD BENCHMARK RESULTS")
    print("=" * 65)
    print(f"  Overall Accuracy : {acc*100:.2f}% (vs 95.16% baseline)")
    print(f"  Precision        : {precision*100:.2f}% (reliability when flagging scams)")
    print(f"  Recall (Catch)   : {recall*100:.2f}% (scam detection rate)")
    print(f"  F1-Score         : {f1*100:.2f}%")
    print(f"  ROC-AUC          : {roc_auc*100:.2f}%")
    print(f"\n  Confusion Matrix across all {total_samples:,} samples:")
    print(f"    True Negatives  (Real Jobs Approved)    : {tn:,}")
    print(f"    False Positives (Real Jobs Flagged)     : {fp:,}")
    print(f"    False Negatives (Scams Missed)          : {fn:,}")
    print(f"    True Positives  (Scams Caught)          : {tp:,}")

    metrics_dict = {
        "model_info": {
            "name": "RandomForestClassifier (Balanced)",
            "file": MODEL_PATH,
            "vectorizer": VECTORIZER_PATH,
            "evaluation_method": f"{N_SPLITS}-Fold Stratified Cross-Validation (Leak-Free)",
            "decision_threshold": DECISION_THRESHOLD
        },
        "dataset_info": {
            "total_samples": int(total_samples),
            "legitimate_jobs": int(legit_count),
            "fraudulent_jobs": int(fraud_count),
            "fraud_rate_pct": round(float(fraud_rate), 2),
            "baseline_accuracy_pct": round(float(100 - fraud_rate), 2),
            "evaluation_folds": N_SPLITS,
            "test_samples": int(total_samples)
        },
        "metrics": {
            "accuracy": round(float(acc) * 100, 2),
            "precision": round(float(precision) * 100, 2),
            "recall": round(float(recall) * 100, 2),
            "f1_score": round(float(f1) * 100, 2),
            "roc_auc": round(float(roc_auc) * 100, 2)
        },
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        },
        "computed_at": datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_dict, f, indent=2)

    print(f"\nMetrics written to: {OUTPUT_PATH}")
    print("=" * 65)


if __name__ == "__main__":
    main()
