# models/archive/README.txt
#
# This directory contains archived / experimental model files
# that are NOT used in production.

# -----------------------------------------------------------------
# job_fraud_model_v2.pkl  (40 KB)
# -----------------------------------------------------------------
# An earlier, smaller model — likely Logistic Regression or a
# lightweight classifier — trained during initial experimentation.
#
# It was superseded by job_fraud_model.pkl (RandomForestClassifier,
# 17.6 MB) which achieves:
#   Accuracy:  99.69%
#   Precision: 100.00%
#   Recall:    93.64%
#   F1 Score:  96.72%
#   ROC-AUC:   99.96%
#
# The production app (app.py) loads:
#   models/job_fraud_model.pkl     <- active model
#   models/tfidf_vectorizer.pkl    <- active vectorizer
#
# Do NOT delete this file unless you are certain it is no longer needed.
