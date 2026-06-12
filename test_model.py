import joblib

model = joblib.load("models/job_fraud_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

job_text = """
Position: Data Entry Executive

Company: Bright Future Solutions

Location: Remote

Description:
We are hiring Data Entry Executives to work from home.
No experience required.
Earn ₹50,000–₹80,000 per month with flexible hours.
Training provided.
Immediate joining available.
"""

X = vectorizer.transform([job_text])

prediction = model.predict(X)[0]
probability = model.predict_proba(X)[0]

print("Prediction:", prediction)
print("Probabilities:", probability)