# scripts/train_model.py
#
# Retrains the production ML model using balanced class weighting
# to effectively detect fraudulent job postings in imbalanced data.
#
# Output:
#   - models/job_fraud_model.pkl
#   - models/tfidf_vectorizer.pkl

import os
import sys
import pandas as pd
import numpy as np
import joblib

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed_jobs.csv")
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "jobs.csv")
MODEL_OUT_PATH = os.path.join(PROJECT_ROOT, "models", "job_fraud_model.pkl")
VEC_OUT_PATH = os.path.join(PROJECT_ROOT, "models", "tfidf_vectorizer.pkl")

# Text columns to combine if raw dataset is used
RAW_TEXT_COLUMNS = ["title", "description", "requirements", "company_profile", "benefits"]


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


def train():
    print("=" * 60)
    print("ShieldJob AI — Production ML Model Training")
    print("=" * 60)

    df = load_dataset()
    df = df.dropna(subset=["fraudulent"])
    
    X_text = extract_text_series(df)
    y = df["fraudulent"].astype(int)

    total_samples = len(df)
    fraud_count = int(y.sum())
    legit_count = int((y == 0).sum())
    fraud_rate = (fraud_count / total_samples) * 100

    print(f"Total Samples : {total_samples:,}")
    print(f"Legitimate    : {legit_count:,} ({100 - fraud_rate:.2f}%)")
    print(f"Fraudulent    : {fraud_count:,} ({fraud_rate:.2f}%)")

    print("\n1. Fitting TF-IDF Vectorizer (max_features=12,000, ngram=(1,2))...")
    vectorizer = TfidfVectorizer(
        max_features=12000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2
    )
    X_vec = vectorizer.fit_transform(X_text)
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_):,} features")

    print("\n2. Training Balanced RandomForestClassifier (n_estimators=100, class_weight='balanced')...")
    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_vec, y)

    os.makedirs(os.path.join(PROJECT_ROOT, "models"), exist_ok=True)

    print(f"\n3. Saving vectorizer -> {VEC_OUT_PATH}")
    joblib.dump(vectorizer, VEC_OUT_PATH)

    print(f"4. Saving model      -> {MODEL_OUT_PATH}")
    joblib.dump(model, MODEL_OUT_PATH)

    print("\nTraining completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    train()
