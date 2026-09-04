# ShieldJob AI — Comprehensive Project Context & Future Handoff

> **To resume work in any new session:**
> Simply tell the AI: *"Read `PROJECT_CONTEXT_HANDOFF.md` and continue our work."*

---

## 1. Project Overview
**ShieldJob AI** is a multi-pillar Fake Job & Employment Scam Detection system built using **Flask (Python)**, **Scikit-Learn (Random Forest Classifier)**, **Google Gemini AI**, **BeautifulSoup web scraping**, and **social reputation verification**.

### Primary URL:
- Local Server: `http://127.0.0.1:5000`

---

## 2. Multi-Pillar Architecture & Scoring Formula

The final safety score (0–100) combines 4 independent verification layers:

$$\text{Safety Score} = (\text{ML Model} \times 0.30) + (\text{Gemini AI} \times 0.30) + (\text{Website} \times 0.20) + (\text{Reputation} \times 0.20)$$

- **Score 70–100**: Looks Legitimate — Safe to Apply (Emerald)
- **Score 50–69**: Suspicious — Proceed with Caution (Amber)
- **Score 0–49**: High Risk — Likely a Scam (Rose/Red)

---

## 3. Production ML Model & Verified Benchmark Metrics
- **Model Type**: `RandomForestClassifier` (100 estimators, `class_weight='balanced'`, random_state=42)
- **Feature Extraction**: `TfidfVectorizer` (ngram_range=(1,2), max_features=12,000, sublinear_tf=True, min_df=2)
- **Dataset**: 17,880 historical job postings (`data/processed_jobs.csv`)
- **Evaluation Methodology**: 5-Fold Stratified Cross-Validation (Out-of-Fold, Leak-Free)
- **Calibrated Fraud Threshold**: 0.30 (Optimized for imbalanced fraud recall)
- **Production Model File**: `models/job_fraud_model.pkl`
- **Vectorizer File**: `models/tfidf_vectorizer.pkl`

### Verified 5-Fold Cross-Validation Metrics:
- **Accuracy**: 97.52% (vs 95.16% majority class baseline)
- **Recall (Scam Catch Rate)**: 85.33% (Catches >85% of all fraud cases across 5 out-of-fold evaluations)
- **Precision**: 69.98% (Reliable scam identification with minimal false alarms)
- **F1 Score**: 76.90% (Balanced harmonic mean for imbalanced fraud detection)
- **ROC-AUC**: 98.49% (High discrimination power across probability thresholds)
- **Out-of-Fold Confusion Matrix (17,880 total)**: 
  - True Negatives (Real Jobs Approved): 16,697
  - False Positives (Real Jobs Flagged): 317
  - False Negatives (Scams Missed): 127
  - True Positives (Scams Caught): 739

---

## 4. Key Improvements Implemented (Summary)

1. **Reputation / Social Verification (`services/social_media_analyzer.py`)**:
   - Live Search API integration (`search_service.py` supporting Brave Search / Google CSE).
   - Seamless fallback to **AI Knowledge Mode** with strict confidence scoring, known-entity checks, and honest caveats.
2. **Resilient Error Handling (`services/gemini_service.py`)**:
   - Structured error dicts (`quota`, `timeout`, `api_key`).
   - Graceful degradation: Continues in ML-only mode without crashing if Gemini quotas are exceeded.
3. **Multi-Page SPA Navigation (`templates/index.html` & `static/style.css`)**:
   - 4 distinct views: **Job Checker (`#analyzer`)**, **Scan History (`#history`)**, **Accuracy & Proof (`#metrics`)**, and **How It Works (`#how-it-works`)**.
   - URL hash routing without page reload.
4. **Scan History with Full Job Description View**:
   - Stores up to 15 entries in `localStorage`.
   - Clickable job snippet in the table opens an interactive **Job Details Modal** with "Copy Text" and "Re-Scan This Job" buttons.
5. **Unified Safety Score Validation across Web & Extension**:
   - Both Web App and Chrome Extension use the identical unified 0–100 safety scoring system:
     - **Score $\ge 70$**: Legitimate / Real Job (Safe, Emerald Green)
     - **Score $50 - 69$**: Suspicious (Proceed with Caution, Amber)
     - **Score $< 50$**: High Risk / Scam (Do not apply, Rose/Red)
   - Streamlined actions: Instant 1-click clipboard summary export and local scan history tracking.

---

## 5. File Structure Reference

```
Fake_Job_Detection/
├── app.py                         # Main Flask application & routes (/, /api/model-metrics)
├── .env                           # API keys (GEMINI_API_KEY, BRAVE_SEARCH_API_KEY, GOOGLE_CSE)
├── PROJECT_CONTEXT_HANDOFF.md     # This comprehensive handoff document
├── requirements.txt               # Dependencies (Flask, scikit-learn, joblib, requests, etc.)
│
├── services/
│   ├── gemini_service.py          # Centralized Gemini client with typed error handling
│   ├── content_validator.py       # AI content audit (tone, salary realism, fee checks)
│   ├── reason_generator.py        # Generates human-readable explainability bullet points
│   ├── website_analyzer.py        # Scrapes and audits company website URLs
│   ├── social_media_analyzer.py   # Dual-mode (Live search / AI knowledge reputation check)
│   ├── search_service.py          # Multi-provider web search wrapper (Brave / Google CSE)
│   └── company_extractor.py       # 3-layer company name parser (regex -> context -> AI fallback)
│
├── models/
│   ├── job_fraud_model.pkl        # Production RandomForest model
│   ├── tfidf_vectorizer.pkl       # Production TF-IDF vectorizer
│   ├── model_metrics.json         # Real computed validation metrics
│   └── archive/
│       ├── job_fraud_model_v2.pkl # Archived unused model
│       └── README.txt             # Archive explanation
│
├── scripts/
│   └── evaluate_model.py          # Standalone model evaluation script
│
├── templates/
│   └── index.html                 # Complete 4-page SPA UI with modals & PDF export
│
└── static/
    └── style.css                  # Cyber Sentinel design system & responsive styling
```

---

## 6. Next Planned Feature: Chrome Extension

### Concept:
A Google Chrome extension allowing users to scan job postings directly on LinkedIn, Indeed, Naukri, and Internshala with 1 click.

### Planned Architecture:
1. **Backend Endpoint**: Add `@app.route('/api/analyze-job', methods=['POST'])` in `app.py`.
2. **`extension/manifest.json`**: Manifest V3 extension configuration.
3. **`extension/content.js`**: Injects floating "🛡️ ShieldJob AI" button into LinkedIn / job portals to extract text and trigger analysis.
4. **`extension/popup.html`**: Mini-dashboard popup showing the safety score gauge and red flags.
5. **Deployment Options**:
   - Free cloud backend hosting on **Render** / **Railway** (`https://shieldjob-api.onrender.com`).
   - Distribution via Chrome Web Store or unpacked developer zip.

---
*Created on August 31, 2026 for ShieldJob AI project continuity.*
