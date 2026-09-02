# ShieldJob AI — Fake Job Detector Chrome Extension

> **Instantly detect fake job postings** — paste a job description, click Analyze, get an AI-powered verdict in seconds.

---

## 🚀 Installation (Developer Mode — No Chrome Web Store needed)

1. **Download** this `fake-job-detector-extension/` folder (or the ZIP)
2. **Extract** the ZIP if needed — you'll have a folder with `manifest.json` inside
3. Open **Google Chrome**
4. Go to `chrome://extensions`
5. Enable **Developer Mode** (toggle in the top-right corner)
6. Click **"Load unpacked"**
7. Select the `fake-job-detector-extension/` folder
8. ✅ The ShieldJob AI icon appears in your Chrome toolbar

---

## 🎯 How to Use

```
1. Visit any job portal (LinkedIn, Naukri, Indeed, Internshala, etc.)
2. Select and COPY the full job description
3. Click the ShieldJob AI shield icon in your Chrome toolbar
4. PASTE the job description into the text area
5. Click "Analyze Job"  (or press Ctrl+Enter)
6. Wait ~10–30 seconds for the AI analysis
7. View the verdict, risk score, and key findings
8. Click "View Full Analysis" for detailed breakdown on the website
```

---

## 📊 What You'll See

| Verdict | Meaning |
|---|---|
| ✅ **LEGITIMATE JOB** | Looks like a real posting — safe to apply |
| ⚠️ **SUSPICIOUS** | Mixed signals — verify the company independently |
| 🚨 **LIKELY FAKE** | High risk — do **not** share personal/banking info |

---

## 🧠 How It Works

The extension sends your job description to the **ShieldJob AI** backend (deployed on Render), which runs:

1. **ML Classifier** — RandomForest trained on 17,880 job postings (99.69% accuracy)
2. **Gemini AI** — Content audit and risk assessment
3. **Reputation Analysis** — Company social/web presence verification
4. **Weighted Score** — Combined safety score (ML 30% + AI 30% + Website 20% + Social 20%)

**Your API keys are never stored in the extension.** All processing happens on the secure backend.

---

## ⚙️ Technical Details

- **Manifest Version**: V3
- **Permissions**: `tabs` (to open the full website), `https://fake-job-detection-iuxn.onrender.com/*`
- **Backend**: `https://fake-job-detection-iuxn.onrender.com/api/extension/analyze`
- **No background scripts**: The extension only runs when you open the popup
- **Privacy**: Your job description is sent to the backend for analysis and is not stored

---

## 🔗 Sharing with Friends

Share the `fake-job-detector-extension/` folder (or zip it):

```bash
# On Windows: right-click the folder → Send to → Compressed (zipped) folder
# Share the ZIP via Google Drive, WhatsApp, email, etc.
```

Recipients follow the same **Installation** steps above.

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Extension doesn't load | Make sure `manifest.json` is directly inside the selected folder |
| "Analysis Failed" error | The Render server may be cold-starting — wait 30 s and try again |
| Very long analysis time | Normal — Render free tier cold-starts can take 30–60 s |
| Empty result | Make sure you pasted the **full** job description (at least 20 characters) |

---

## 📁 File Structure

```
fake-job-detector-extension/
├── manifest.json     ← Extension configuration (Manifest V3)
├── popup.html        ← Extension popup UI
├── popup.css         ← Styling
├── popup.js          ← All logic (API calls, rendering, error handling)
├── icons/
│   ├── icon16.png    ← Toolbar icon (small)
│   ├── icon48.png    ← Extension management icon
│   └── icon128.png   ← Chrome Web Store icon
└── README.md         ← This file
```

---

## 🔮 Future (Version 2)

In a future version, the extension may automatically detect and extract job descriptions from LinkedIn, Naukri, Indeed, and other portals — eliminating the need to copy-paste manually.

---

*Built on top of ShieldJob AI — deployed at https://fake-job-detection-iuxn.onrender.com/*
