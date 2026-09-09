# -*- coding: utf-8 -*-
"""
Full PDF generation script for ShieldJob AI Internship Review Preparation Guide.
"""
import os
import subprocess

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ShieldJob AI — Comprehensive Internship Review Preparation Guide</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {
      content: counter(page);
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: #64748b;
    }
  }

  * {
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.55;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }

  /* Cover / Header */
  .doc-header {
    border-bottom: 3px solid #3b82f6;
    padding-bottom: 16px;
    margin-bottom: 24px;
  }
  .doc-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1e40af, #3b82f6);
    color: #ffffff;
    font-size: 8pt;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }
  .doc-title {
    font-size: 20pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 6px 0;
    line-height: 1.2;
  }
  .doc-subtitle {
    font-size: 11pt;
    font-weight: 500;
    color: #475569;
    margin: 0 0 12px 0;
  }
  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    font-size: 8.5pt;
  }
  .meta-item strong {
    color: #0f172a;
    display: block;
    font-size: 7.5pt;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 2px;
  }

  /* Headings */
  h1 {
    font-size: 14pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    page-break-after: avoid;
  }
  h2 {
    font-size: 11.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 18px;
    margin-bottom: 8px;
    border-left: 4px solid #3b82f6;
    padding-left: 8px;
    page-break-after: avoid;
  }
  h3 {
    font-size: 10pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 8px;
  }

  /* Speaking Script Box */
  .script-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0284c7;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }
  .script-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    border-bottom: 1px dashed #cbd5e1;
    padding-bottom: 4px;
  }
  .slide-tag {
    font-weight: 700;
    font-size: 9pt;
    color: #0369a1;
  }
  .slide-duration {
    font-size: 8pt;
    color: #64748b;
    font-weight: 600;
  }
  .spoken-text {
    font-size: 9.5pt;
    color: #0f172a;
    line-height: 1.6;
    font-style: italic;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 8px 12px;
    margin-top: 6px;
    margin-bottom: 8px;
  }
  .spoken-text strong {
    font-style: normal;
    color: #1e3a8a;
  }
  .visual-guide {
    background: #f1f5f9;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 8.5pt;
    margin-top: 6px;
  }
  .visual-guide strong {
    color: #334155;
  }

  /* QA Block */
  .qa-block {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    page-break-inside: avoid;
  }
  .qa-q {
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 4px;
    font-size: 9.5pt;
  }
  .qa-q .q-badge {
    background: #e0f2fe;
    color: #0369a1;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 1px 6px;
    border-radius: 3px;
    margin-right: 4px;
  }
  .qa-a {
    color: #334155;
    font-size: 9pt;
    line-height: 1.5;
    padding-left: 8px;
    border-left: 2px solid #38bdf8;
  }

  /* Probability Badges */
  .prob-vh {
    border-left: 4px solid #ef4444 !important;
    background: #fef2f2;
  }
  .prob-h {
    border-left: 4px solid #f59e0b !important;
    background: #fffbeb;
  }
  .prob-p {
    border-left: 4px solid #eab308 !important;
    background: #fefce8;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin-top: 8px;
    margin-bottom: 14px;
    page-break-inside: avoid;
  }
  th {
    background: #1e293b;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #1e293b;
    font-size: 8pt;
  }
  td {
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background: #f8fafc;
  }

  /* Highlight Cards / Callouts */
  .info-card {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #2563eb;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-size: 8.5pt;
  }
  .success-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #16a34a;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-size: 8.5pt;
  }
  .warning-card {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid #d97706;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-size: 8.5pt;
  }

  .page-break {
    page-break-before: always;
  }

  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  code {
    font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8pt;
    color: #0f172a;
  }
</style>
</head>
<body>

<!-- COVER / HEADER -->
<div class="doc-header">
  <div class="doc-badge">Official Internship Review Defense & Speaking Manual</div>
  <h1 class="doc-title">ShieldJob AI: Multi-Modal Fake Job Detection System</h1>
  <div class="doc-subtitle">Complete Slide-by-Slide Script • Live Project Demo • Comprehensive Review Q&A • Consistency Check • Final Cheat Sheet</div>
  
  <div class="meta-grid">
    <div class="meta-item">
      <strong>Candidate Name</strong>
      Tanuku Ram Sai
    </div>
    <div class="meta-item">
      <strong>PIN / Regd. No.</strong>
      24A95A0503
    </div>
    <div class="meta-item">
      <strong>Department & College</strong>
      Dept. of CSE, Aditya University
    </div>
    <div class="meta-item">
      <strong>Internship Company</strong>
      VedXlence Innovations Pvt. Ltd., Hyderabad
    </div>
  </div>
</div>

<!-- PART 1 -->
<h1>PART 1 — Slide-by-Slide Speaking Script (15 Slides)</h1>
<p><em>Use this exact script while presenting the PPT. Each slide is structured for 30–90 seconds of clear, natural, spoken delivery with precise transitions and visual callout directions for diagrams and screenshots.</em></p>

<!-- Slide 1 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 1 — Title Slide (Internship Project Report on ShieldJob AI)</span>
    <span class="slide-duration">⏱️ ~30 Seconds</span>
  </div>
  <div class="spoken-text">
    "Respected review panel members and faculty, a very pleasant morning/afternoon to everyone. My name is <strong>Tanuku Ram Sai</strong>, bearing Roll Number <strong>24A95A0503</strong> from the Department of Computer Science and Engineering at Aditya University. Today, I am proud to present my AICTE-certified Summer Internship project titled <strong>'ShieldJob AI: A Multi-Modal Fake Job Detection System'</strong>. This project was developed during my two-month internship at <strong>VedXlence Innovations Pvt. Ltd., Hyderabad</strong>, under the domain of Machine Learning with Python. In this presentation, I will walk you through the real-world problem of recruitment fraud, our four-layer AI/ML architecture, live deployment on the cloud, and practical browser extension integration."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 2:</strong> "Let me begin by giving you a high-level executive summary of the project."
  </div>
</div>

<!-- Slide 2 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 2 — Abstract</span>
    <span class="slide-duration">⏱️ ~45-60 Seconds</span>
  </div>
  <div class="spoken-text">
    "Looking at the abstract, the rapid migration of hiring processes to digital platforms like LinkedIn, Indeed, and Naukri has unfortunately resulted in an alarming increase in online employment scams. Fraudulent actors create convincing job posts with spoofed company domains and unrealistic salary offers to extort money and steal identities. To address this, <strong>ShieldJob AI</strong> introduces a multi-modal verification system that evaluates any job posting across <strong>four specialized safety layers</strong>: a Balanced Random Forest ML model, Google Gemini AI contextual auditing, automated company website scraping, and live social footprint verification. The system delivers an instant 0 to 100 risk score and safety badges through both a responsive Flask web application and a 1-click Chrome Extension. It achieves an impressive <strong>98.05% accuracy</strong> on 17,880 benchmark job postings."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 3:</strong> "Now, let us examine the real-world background and motivation that drove this project."
  </div>
</div>

<!-- Slide 3 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 3 — Introduction</span>
    <span class="slide-duration">⏱️ ~45-60 Seconds</span>
  </div>
  <div class="spoken-text">
    "In today's digital hiring landscape, finding a job online is faster than ever, but it has also created massive vulnerabilities. Scammers now use sophisticated social engineering: they publish fake listings, conduct informal interviews over Telegram or WhatsApp, and demand upfront fees under the guise of 'training fees', 'onboarding laptop security', or 'registration charges'. Traditional keyword filters fail because modern scam job descriptions use well-written corporate language. Meanwhile, job seekers lack the technical capability to manually verify domain registration ages, SSL certificates, or official corporate filings. ShieldJob AI automates this entire cross-verification in seconds, giving students and job seekers an instant in-browser safety shield before they share sensitive personal data or hard-earned money."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 4:</strong> "Let us now clearly define the exact problem statement we are solving."
  </div>
</div>

<!-- Slide 4 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 4 — Problem Statement</span>
    <span class="slide-duration">⏱️ ~45-60 Seconds</span>
  </div>
  <div class="spoken-text">
    "Our problem statement centers around four critical industry vulnerabilities. First, thousands of fresh graduates fall victim annually to predatory recruitment scams. Second, financial extortion occurs through upfront fee demands disguised as document processing or onboarding deposits. Third, bad actors practice company impersonation through typosquatting—creating look-alike website domains that deceive unwary applicants. And fourth, existing solutions rely on single-layer checks. If you only check text, you miss fake company websites; if you only check website domains, you miss fraudulent text descriptions. Therefore, there is an urgent need for an instant, multi-modal defense tool that delivers clear <strong>Safe</strong>, <strong>Suspicious</strong>, or <strong>Fake</strong> verdicts in real time directly inside the user's browser."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 5:</strong> "To solve these challenges, here is an overview of the ShieldJob AI ecosystem."
  </div>
</div>

<!-- Slide 5 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 5 — Project Overview</span>
    <span class="slide-duration">⏱️ ~60 Seconds</span>
  </div>
  <div class="spoken-text">
    "ShieldJob AI is designed as an end-to-end intelligent detection ecosystem. It is powered by <strong>four specialized analytical pillars</strong>: First, our <strong>Machine Learning Pattern Matcher</strong> weighted at 30%, trained on historical scam syntax. Second, our <strong>Generative AI Content Inspector</strong> using Google Gemini at 30%, which audits tone anomalies and fee-extortion semantics. Third, the <strong>Website Authenticity Verifier</strong> at 20%, checking live domain existence and business legitimacy. And fourth, the <strong>Company Reputation Analyzer</strong> at 20%, auditing LinkedIn and social footprints. These four layers combine into a unified 0 to 100 Safety Score. We provide dual interfaces: a full-featured Flask Web App for comprehensive audits and a 1-click Chrome Extension for frictionless in-browser verification with transparent explainability bullets."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 6:</strong> "Let us dive into the technical methodology and data pipeline behind these four layers."
  </div>
</div>

<!-- Slide 6 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 6 — Methodology</span>
    <span class="slide-duration">⏱️ ~60-75 Seconds</span>
  </div>
  <div class="spoken-text">
    "Our methodology follows a rigorous 5-step engineering pipeline. In <strong>Step 1</strong>, we preprocessed 17,880 job records from the benchmark EMSCAD dataset, extracting 12,000 unigram and bigram features via sublinear TF-IDF. In <strong>Step 2</strong>, we trained a Balanced Random Forest Classifier with balanced class weights to resolve the severe 4.84% scam class imbalance. In <strong>Step 3</strong>, we engineered structured prompts for Google Gemini 2.5 Flash to spot semantic red flags like unrealistic salaries and hidden fee requests. In <strong>Step 4</strong>, we integrated BeautifulSoup for automated website scraping and Brave Search/Google CSE for live social verification. Finally, in <strong>Step 5</strong>, our aggregation engine calculates the final Safety Score as 30% ML plus 30% Gemini AI plus 20% Website plus 20% Social verification."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 7:</strong> "Now, let us examine the complete system architecture diagram."
  </div>
</div>

<!-- Slide 7 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 7 — System Architecture</span>
    <span class="slide-duration">⏱️ ~75-90 Seconds</span>
  </div>
  <div class="spoken-text">
    "This slide illustrates the multi-pillar architecture of ShieldJob AI. When the user inputs a job description and optional company URL, our system distributes the payload into four parallel processing channels. The <strong>ML model</strong> analyzes statistical n-gram patterns. Concurrently, <strong>Gemini AI</strong> evaluates the contextual legitimacy and recruiter tone. Simultaneously, the <strong>Website Check</strong> scrapes the domain with BeautifulSoup to verify active operations, while the <strong>Social Check</strong> searches LinkedIn and public scam databases. All four independent probability outputs feed into our <strong>Score Aggregation Engine</strong>, producing a final weighted score mapped to three clear badges: Emerald for Legitimate (70 to 100), Amber for Suspicious (50 to 69), and Rose/Red for Likely Fake (below 50)."
  </div>
  <div class="visual-guide">
    <strong>What to point at on Slide 7:</strong><br>
    • <strong>Top Block:</strong> Point to "User Input" where job description and company URL enter.<br>
    • <strong>Middle 4 Boxes:</strong> Point to the 4 parallel pillars (30% ML, 30% Gemini AI, 20% Website, 20% Social).<br>
    • <strong>Bottom Aggregation Engine:</strong> Point to the weighted formula and the 3 final classification badge outputs.
  </div>
</div>

<!-- Slide 8 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 8 — System Structure & Workflow</span>
    <span class="slide-duration">⏱️ ~60-75 Seconds</span>
  </div>
  <div class="spoken-text">
    "Here is the step-by-step user workflow in practice. First, while browsing portals like LinkedIn, Naukri, or Unstop, the user encounters a job listing. Second, they open the 1-click ShieldJob Chrome Extension and paste the description. Third, the extension dispatches a secure HTTPS payload to our Flask REST API hosted on Render. Crucially, zero API keys are exposed in the client extension. Fourth, the cloud backend triggers the four-layer multi-modal audit in parallel. And fifth, within two to three seconds, the user receives an instant diagnostic verdict with the Safety Score gauge, risk breakdown, and actionable red flag warnings."
  </div>
  <div class="visual-guide">
    <strong>What to point at on Slide 8:</strong> Trace the 5 numbered steps from left to right: (1) Browse Job Portal &rarr; (2) Chrome Extension Popup &rarr; (3) Flask Cloud API on Render &rarr; (4) Parallel Multi-Layer Scan &rarr; (5) Instant Verdict & Red Flags.
  </div>
</div>

<!-- Slide 9 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 9 — Implementation & Tech Stack</span>
    <span class="slide-duration">⏱️ ~60 Seconds</span>
  </div>
  <div class="spoken-text">
    "Looking at our implementation technologies: On the backend, we utilized <strong>Python 3.11 with Flask REST API</strong>, Gunicorn WSGI server, and CORS handling. For Machine Learning, we used <strong>Scikit-Learn</strong>, implementing TF-IDF vectorization and Random Forest classification with Joblib serialization. For Generative AI, we integrated the <strong>Google Gemini API</strong> using the official Python SDK. For live web and reputation verification, we used <strong>BeautifulSoup</strong> and search APIs. On the frontend, we built a modern glassmorphism UI with HTML5, Vanilla CSS3, ES6 JavaScript, and developed the <strong>Chrome Extension under Manifest V3</strong> standards. The complete system is deployed live on <strong>Render Cloud</strong> with automated CI/CD."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 10:</strong> "Let us now examine the benchmark experimental results and validation metrics."
  </div>
</div>

<!-- Slide 10 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 10 — Results: Model Accuracy & Proof</span>
    <span class="slide-duration">⏱️ ~75-90 Seconds</span>
  </div>
  <div class="spoken-text">
    "We evaluated our machine learning pipeline using <strong>5-Fold Stratified Out-of-Fold Cross-Validation</strong> across all 17,880 dataset samples to guarantee zero data leakage. The results show outstanding performance: an overall <strong>Accuracy of 98.05%</strong>, a <strong>Scam Recall (Catch Rate) of 81.29%</strong>, a <strong>Precision of 79.10%</strong>, an <strong>F1-Score of 80.18%</strong>, and a <strong>ROC-AUC of 98.49%</strong>. Looking at our confusion matrix, out of 17,014 genuine jobs, 16,828 were correctly approved with only a 1.1% false alarm rate. Out of 866 real fraudulent postings, our model successfully detected 704 scams. This demonstrates that our calibrated threshold of 0.24 provides a robust balance between high scam detection and minimal false alarms."
  </div>
  <div class="visual-guide">
    <strong>What to point at on Slide 10:</strong><br>
    • <strong>Top Metrics:</strong> Point to 98.05% Accuracy and 81.29% Recall.<br>
    • <strong>Confusion Matrix:</strong> Highlight True Negatives (16,828 real jobs approved) and True Positives (704 scams caught out of 866). Emphasize the low False Positive rate (186 / 1.1%).
  </div>
</div>

<!-- Slide 11 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 11 — Results: Live App & Extension in Action</span>
    <span class="slide-duration">⏱️ ~60-75 Seconds</span>
  </div>
  <div class="spoken-text">
    "This slide demonstrates our working software artifacts in action. On the left, you can see the <strong>Google Chrome Extension</strong> verifying a live job posting from Unstop for a Cisco position. The extension instantly displays a verified Legitimate status with a 75.8 Safety Score and 91% ML confidence. On the right, you can see our <strong>Scan History Dashboard</strong> on the web application, which logs analyzed jobs with interactive safety badges, timestamped audit summaries, and one-click re-scan capabilities. This proves that ShieldJob AI is not just a theoretical model, but a fully functional, cloud-deployed product."
  </div>
  <div class="visual-guide">
    <strong>What to point at on Slide 11:</strong><br>
    • <strong>Left Screenshot:</strong> Point to the Chrome Extension popup showing the 75.8 score and green Legitimate badge.<br>
    • <strong>Right Screenshot:</strong> Point to the web dashboard scan history table showing recent job scans and color badges.
  </div>
</div>

<!-- Slide 12 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 12 — Challenges & Learning Outcomes</span>
    <span class="slide-duration">⏱️ ~60 Seconds</span>
  </div>
  <div class="spoken-text">
    "During development, we solved three major technical challenges. First, <strong>extreme class imbalance</strong>—scams represent only 4.84% of the dataset. We resolved this using balanced class weighting and stratified sampling. Second, <strong>unstructured text data</strong> with missing fields, which we standardized through regex pipelines and sublinear TF-IDF scaling. Third, <strong>cloud cold starts and external API latency</strong>, which we addressed by executing API calls in parallel and implementing graceful fallback modes so the system never crashes. Through this project, I gained hands-on industry mastery in end-to-end ML pipelines, LLM prompt engineering, Manifest V3 browser extension development, and production cloud deployment."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 13:</strong> "Let us conclude with the project summary and future scope."
  </div>
</div>

<!-- Slide 13 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 13 — Conclusion & Future Scope</span>
    <span class="slide-duration">⏱️ ~60 Seconds</span>
  </div>
  <div class="spoken-text">
    "In conclusion, ShieldJob AI proves that combining classical Machine Learning with Generative AI and live digital footprint auditing creates a robust, multi-layered defense against modern recruitment fraud. By delivering both a web platform and a Chrome Extension, we make enterprise-grade verification accessible to every student with a single click. In the future, we plan to implement <strong>automated DOM scraping</strong> to highlight scam postings on job portals automatically without copy-pasting, expand to <strong>multilingual NLP models</strong> for regional Indian languages, integrate official corporate registry checks via the Ministry of Corporate Affairs (MCA), and develop a WhatsApp bot for instant mobile verification."
  </div>
  <div class="visual-guide">
    <strong>Transition to Slide 14 & 15:</strong> "Here are our key academic and technical references."
  </div>
</div>

<!-- Slide 14 & 15 -->
<div class="script-card">
  <div class="script-header">
    <span class="slide-tag">Slide 14 & 15 — References & Thank You</span>
    <span class="slide-duration">⏱️ ~30 Seconds</span>
  </div>
  <div class="spoken-text">
    "Our work is grounded in established research, including Scikit-Learn literature by Pedregosa et al., Google's Gemini technical papers, Chrome Manifest V3 documentation, and the benchmark EMSCAD dataset. With this, I conclude my presentation. I want to express my sincere gratitude to my project guide, Mr. M. Srinu, Head of the Department Dr. T. Sudha Rani, faculty members, and VedXlence Innovations for their support. I am now open to your questions and valuable feedback. Thank you!"
  </div>
</div>

<!-- PART 2 -->
<div class="page-break"></div>
<h1>PART 2 — Live Project Demonstration Script (12 Sections)</h1>
<p><em>Follow this step-by-step spoken script when demonstrating the live ShieldJob AI web application and Chrome extension to the reviewers.</em></p>

<div class="qa-block">
  <div class="qa-q">1. Demo Introduction</div>
  <div class="qa-a">
    "Now, I would like to demonstrate the live, fully functional ShieldJob AI system. The web application is deployed on the Render cloud platform at <code>https://fake-job-detection-iuxn.onrender.com</code>, and we also have our Chrome Extension running locally in developer mode under Manifest V3 standards. I will show how our four-pillar system processes both genuine and fraudulent job postings in real time."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">2. Application / Home Page Interface</div>
  <div class="qa-a">
    "Here is the main landing page and analyzer dashboard of ShieldJob AI. It features a modern, responsive cyber-themed glassmorphism interface built with Vanilla CSS. At the top, we have our navigation bar with quick links to the Analyzer, System Architecture, Live Proof & Accuracy metrics, and Scan History. The primary input card provides fields for the Job Title, Job Description, and an optional Company Website URL for live domain auditing."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">3. User Input</div>
  <div class="qa-a">
    "To demonstrate, let us take a suspicious job posting that promises a high salary for a data entry role but mentions an upfront 'laptop training kit fee' and provides an unverified contact email. I paste the job title 'Remote Data Entry Associate' and the full job description into the text area, and enter the provided company website URL. Now, I will click the 'Analyze Job' button."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">4. Analysis Process</div>
  <div class="qa-a">
    "When I click 'Analyze Job', the frontend sends an asynchronous POST request to our Flask backend route. The backend immediately dispatches four concurrent analysis tasks: tokenizing the text for our Random Forest model, querying the Google Gemini 2.5 Flash API with custom fraud-auditing prompts, initiating BeautifulSoup to scrape and inspect the company domain, and querying search APIs for social footprints."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">5. Machine Learning Prediction Layer</div>
  <div class="qa-a">
    "First, our serialized TF-IDF vectorizer converts the input text into a 12,000-dimensional unigram/bigram feature vector with sublinear term-frequency scaling. Our Balanced Random Forest model evaluates statistical n-gram probabilities against the 17,880 historical patterns learned during training, outputting a machine learning safety probability score."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">6. Gemini AI Contextual Validation Layer</div>
  <div class="qa-a">
    "Simultaneously, Google Gemini 2.5 Flash acts as a semantic fraud investigator. While the ML model looks at word frequencies, Gemini reads the text contextually. In this sample, Gemini immediately flags the requirement of an upfront training deposit, the inflated salary of $45/hour for basic typing, and informal communication channels, returning a detailed JSON risk payload."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">7. Website Analysis Layer</div>
  <div class="qa-a">
    "Next, our Website Analyzer service fetches the target URL using BeautifulSoup with custom browser headers. It evaluates domain structure, meta-tags, and body content to verify whether the domain belongs to an active, legitimate corporate entity or is an empty shell page registered to deceive applicants."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">8. Social Media Analysis Layer</div>
  <div class="qa-a">
    "Concurrently, the Social Media Verifier queries Brave Search and Google CSE for the company's verified LinkedIn page, Glassdoor employee reviews, and scam alert mentions on forums like Reddit. If search quotas are limited, it automatically falls back to Gemini AI Knowledge Mode to audit public reputation."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">9. Final Risk Score & Verdict Presentation</div>
  <div class="qa-a">
    "Our Score Aggregation Engine combines all four weighted outputs: 30% ML, 30% Gemini AI, 20% Website, and 20% Social. As you can see on the screen, the system calculated an overall Safety Score of <strong>28 out of 100</strong>, displaying a prominent <strong>Rose/Red 'Likely Fake'</strong> alert badge with an interactive circular SVG gauge."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">10. Explanation / Red Flags Diagnostic</div>
  <div class="qa-a">
    "Below the safety score gauge, ShieldJob AI provides transparent, human-readable explainability bullets. It explicitly lists the exact red flags detected: 'Demands upfront onboarding fee', 'Unrealistic salary for entry-level work', 'Domain lack of corporate history', and 'High statistical similarity to known scam templates'. This transparency helps the student understand exactly why the job was flagged."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">11. Other Important Features (Scan History & Chrome Extension Demo)</div>
  <div class="qa-a">
    "If we scroll down, you can see the <strong>Scan History Dashboard</strong>, which logs every analyzed job with timestamps, score badges, and re-scan options. Now, let me switch to a live job portal in Google Chrome. When I click the <strong>ShieldJob AI Chrome Extension</strong> icon, a compact popup opens. I paste the job text, click Analyze, and within 2 seconds, the extension renders the identical 4-pillar risk score directly inside the browser window via our lightweight REST API."
  </div>
</div>

<div class="qa-block">
  <div class="qa-q">12. Demo Conclusion</div>
  <div class="qa-a">
    "This completes the live demonstration of ShieldJob AI. We have seen how the Flask web application and the Manifest V3 Chrome Extension seamlessly leverage Machine Learning, Gemini AI, website scraping, and social auditing to protect job seekers in real time. Thank you, and I am ready for the technical Q&A session."
  </div>
</div>

<!-- PART 3 -->
<div class="page-break"></div>
<h1>PART 3 — Comprehensive Internship Review Q&A (45 Topic Areas)</h1>
<p><em>Every question contains a concise, technically correct, natural answer tailored for a 2-5 sentence spoken response during review.</em></p>

<!-- Topics 1 - 10 -->
<div class="qa-block">
  <div class="qa-q"><span class="q-badge">01</span> General Project: What is ShieldJob AI in simple terms?</div>
  <div class="qa-a">"ShieldJob AI is a multi-modal cybersecurity and fake job detection platform. It uses a four-pillar approach—combining classical Machine Learning, Google Gemini Generative AI, live website scraping, and social reputation auditing—to determine whether an online job posting is genuine, suspicious, or a scam. It delivers instant 0 to 100 safety scores through a web app and Chrome extension."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">02</span> Internship & Organization: Where did you do your internship and for how long?</div>
  <div class="qa-a">"I completed a 2-month AICTE-certified internship from May 6, 2026, to July 5, 2026, at VedXlence Innovations Pvt. Ltd., located in Hyderabad. The internship domain was Machine Learning with Python, structured into an initial technical upskilling phase followed by full-stack real-world project implementation."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">03</span> Problem Statement: What specific problem does your project address?</div>
  <div class="qa-a">"With hiring moving online, scammers create convincing job postings on platforms like LinkedIn and Naukri to steal personal identity data and extort upfront registration or training fees. Traditional keyword filters fail to catch modern scam phrasing, and manual background checks are too difficult for everyday students. ShieldJob AI provides an automated, real-time safety verification tool."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">04</span> Motivation: What inspired you to choose fake job detection?</div>
  <div class="qa-a">"As college students entering the placement season, my peers and I frequently encounter unsolicited recruitment offers demanding registration deposits or suspicious Telegram interviews. Seeing fellow graduates lose money and compromise their personal credentials motivated me to build a practical, accessible AI defense tool."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">05</span> Objectives: What were the primary technical objectives of your project?</div>
  <div class="qa-a">"Our primary objectives were to train a high-accuracy machine learning model on 17,880 historical job records, integrate Google Gemini AI for contextual fraud auditing, implement live website and social verification, and deploy the solution as both a responsive Flask web app and a 1-click Chrome Extension."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">06</span> Proposed Solution: How does your solution differ from existing spam filters?</div>
  <div class="qa-a">"Existing solutions rely on single-layer text filters or static keyword blacklists that miss sophisticated fraud. ShieldJob AI uses a multi-modal 4-pillar approach that simultaneously checks statistical text syntax, LLM semantic reasoning, live domain scraping, and social media footprint, making it virtually impossible for scammers to bypass all safety layers."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">07</span> Technologies Used: What is the complete technology stack of your project?</div>
  <div class="qa-a">"On the backend, we use Python 3.11 with Flask, Gunicorn WSGI, Scikit-Learn for ML, Google Gemini 2.5 Flash API for GenAI, and BeautifulSoup for web scraping. On the frontend, we use HTML5, Vanilla CSS3 with glassmorphism, JavaScript ES6, and Chrome Extension Manifest V3, all hosted on Render Cloud."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">08</span> Technology Selection: Why did you choose Flask instead of Django or FastAPI?</div>
  <div class="qa-a">"Flask is lightweight, modular, and offers minimal overhead for serving our Single-Page Application and microservice REST API endpoints. Since our application does not require a heavy relational ORM or built-in authentication tables, Flask allowed us to build high-speed asynchronous prediction routes with clean architectural boundaries."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">09</span> System Architecture: Explain the 4 pillars of your architecture.</div>
  <div class="qa-a">"The architecture consists of four weighted analytical pillars: Layer 1 is the Balanced Random Forest ML model (30%), Layer 2 is the Gemini 2.5 Flash semantic auditor (30%), Layer 3 is the BeautifulSoup website scraper (20%), and Layer 4 is the search-engine social footprint auditor (20%). Their outputs are aggregated into a final 0 to 100 Safety Score."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">10</span> Project Workflow: What happens internally from the moment a user submits a job?</div>
  <div class="qa-a">"The Flask backend receives the payload and triggers four parallel tasks. The text is vectorized through TF-IDF and passed to Random Forest, Gemini evaluates semantic red flags via API, BeautifulSoup scrapes the company website, and search APIs query LinkedIn. The Score Aggregation Engine computes the weighted score and returns a JSON verdict with explainability bullets."</div>
</div>

<!-- Topics 11 - 20 -->
<div class="qa-block">
  <div class="qa-q"><span class="q-badge">11</span> Machine Learning: What role does classical ML play in your system?</div>
  <div class="qa-a">"Machine learning provides high-speed statistical pattern matching. It analyzes term frequency distributions across 17,880 historical job descriptions to instantly calculate the statistical probability that a text matches known recruitment fraud phrasing without incurring API costs."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">12</span> NLP: What Natural Language Processing techniques did you apply?</div>
  <div class="qa-a">"We implemented text normalization including lowercase conversion, URL tokenization, special character cleaning, and stopword filtering. We then applied TF-IDF feature extraction with unigram and bigram tokenization and sublinear term-frequency scaling across a vocabulary of 12,000 features."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">13</span> TF-IDF: Why did you use TF-IDF and what specific hyperparameters did you choose?</div>
  <div class="qa-a">"TF-IDF converts unstructured text into numerical vectors by weighing terms based on frequency in a document versus frequency across all documents. We configured <code>max_features=12,000</code>, <code>ngram_range=(1,2)</code> to capture two-word phrases like 'wire transfer', <code>sublinear_tf=True</code> to dampen high-frequency terms, and <code>min_df=2</code> to eliminate noise."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">14</span> ML Models: Which machine learning algorithm did you use and why?</div>
  <div class="qa-a">"We used the <strong>Random Forest Classifier</strong> with 100 decision trees. Random Forest is an ensemble learning method that combines multiple decorrelated decision trees, preventing overfitting on high-dimensional text data and providing robust generalization."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">15</span> Model Selection: Why did you select Random Forest over Logistic Regression or Naive Bayes?</div>
  <div class="qa-a">"While Naive Bayes assumes strict feature independence and Logistic Regression finds linear decision boundaries, Random Forest captures complex non-linear feature interactions between multiple job attributes and provides built-in support for balanced class weighting."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">16</span> Training & Testing: How did you train and validate your machine learning model?</div>
  <div class="qa-a">"We trained the model on 17,880 postings from the EMSCAD dataset using <strong>5-Fold Stratified Out-of-Fold Cross-Validation</strong>. Stratified splitting ensured each fold preserved the exact 4.84% scam ratio, and out-of-fold predictions guaranteed zero data leakage between training and evaluation."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">17</span> Accuracy & Evaluation: What are your key evaluation metrics and results?</div>
  <div class="qa-a">"Across all 17,880 benchmark samples, our model achieved <strong>98.05% Accuracy</strong>, <strong>79.10% Precision</strong>, <strong>81.29% Scam Recall</strong>, <strong>80.18% F1-Score</strong>, and <strong>98.49% ROC-AUC</strong>, catching 704 out of 866 real fraud cases with only 186 false alarms."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">18</span> Gemini AI: Which Generative AI model did you integrate and how?</div>
  <div class="qa-a">"We integrated <strong>Google Gemini 2.5 Flash</strong> via the official <code>google-generativeai</code> Python SDK. It is invoked on the backend with engineered prompts and strict JSON schema constraints to return deterministic fraud assessments and explainability bullets."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">19</span> AI Validation: Why is Gemini AI necessary if you already have an ML model?</div>
  <div class="qa-a">"Classical ML only detects statistical n-gram patterns, so if a scammer writes a grammatically perfect job posting, ML alone might miss it. Gemini AI provides deep semantic understanding—it evaluates whether the salary is realistic for the duties, identifies subtle fee-extortion phrasing, and checks recruiter professionalism."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">20</span> Website Analysis: How does your system verify company websites?</div>
  <div class="qa-a">"The Website Analyzer uses BeautifulSoup with custom browser headers to fetch the target domain's HTML. It extracts text, title, and meta tags, and prompts Gemini to audit whether the site represents an active commercial business or an empty shell domain created for typosquatting."</div>
</div>

<!-- Topics 21 - 30 -->
<div class="qa-block">
  <div class="qa-q"><span class="q-badge">21</span> Social Media Analysis: How do you verify social media and company reputation?</div>
  <div class="qa-a">"Our Social Media Verifier extracts the company name and queries Brave Search and Google Custom Search Engine for verified LinkedIn company pages, employee counts, Glassdoor reviews, and Reddit scam reports. If search quotas are unavailable, it seamlessly switches to Gemini AI Knowledge Mode."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">22</span> Risk Scoring: What is your exact mathematical formula for the Safety Score?</div>
  <div class="qa-a">"The formula is: <code>Safety Score = (ML_Score * 0.30) + (Gemini_Score * 0.30) + (Website_Score * 0.20) + (Social_Score * 0.20)</code>. Scores from 70 to 100 are Legitimate (Safe), 50 to 69 are Suspicious (Proceed with Caution), and 0 to 49 are Likely Fake (High Risk)."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">23</span> Flask / Backend: How is the Flask application structured?</div>
  <div class="qa-a">"The Flask app is modularized with clean separation: <code>app.py</code> handles routing and CORS, <code>services/</code> contains dedicated modules for ML inference, Gemini API, website scraping, and social auditing, and <code>models/</code> stores serialized pickle artifacts and evaluation metrics."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">24</span> Frontend: How did you design the user interface?</div>
  <div class="qa-a">"The frontend is built using clean semantic HTML5 and custom Vanilla CSS3 with glassmorphism aesthetics, dynamic SVG gauge animations, and responsive layouts. Asynchronous JavaScript fetch handles non-blocking API communication without page reloads."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">25</span> APIs: What external APIs are used and how do you protect API keys?</div>
  <div class="qa-a">"We use the Google Gemini API and Brave Search / Google CSE APIs. All API keys are securely stored as server-side environment variables on the Render cloud platform. The Chrome Extension communicates only with our Flask API, ensuring zero keys are exposed to clients."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">26</span> Database: How do you handle scan history and persistence?</div>
  <div class="qa-a">"Scan history is stored in-memory and managed through client session and local storage with CSV export capabilities. For a production enterprise deployment, this can be seamlessly migrated to PostgreSQL with SQLAlchemy ORM."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">27</span> Data Preprocessing: What steps were taken to clean the raw dataset?</div>
  <div class="qa-a">"We concatenated title, company profile, description, requirements, and benefits into a single text block, removed missing values, lowercased all text, stripped HTML and URLs using regular expressions, and removed standard English stopwords before TF-IDF vectorization."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">28</span> Dataset: Tell me about the dataset used for training.</div>
  <div class="qa-a">"We used the benchmark Employment Scam Aegean Dataset (EMSCAD / Kaggle Fake Job Postings). It consists of 17,880 real-world job postings with 18 metadata attributes, containing 17,014 legitimate jobs (95.16%) and 866 confirmed fraudulent postings (4.84%)."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">29</span> Feature Extraction: Why did you use unigrams and bigrams together?</div>
  <div class="qa-a">"Unigrams capture isolated keywords like 'fee' or 'wire', but scammers often use innocent individual words that become suspicious only in combination, such as 'wire transfer', 'registration deposit', or 'immediate joining'. Bigrams capture these critical two-word contextual relationships."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">30</span> Deployment: How and where is ShieldJob AI deployed?</div>
  <div class="qa-a">"The backend is deployed as a cloud web service on the Render platform utilizing Python 3.11, Gunicorn WSGI server, automated environment variable injection, and CORS headers allowing secure connections from the Chrome Extension."</div>
</div>

<!-- Topics 31 - 45 -->
<div class="qa-block">
  <div class="qa-q"><span class="q-badge">31</span> Testing: How did you test the backend and extension?</div>
  <div class="qa-a">"We performed unit testing on the ML inference pipeline with sample edge cases, API contract testing on <code>/api/extension/analyze</code> using Postman and curl, and end-to-end user testing of the Chrome Extension popup across LinkedIn, Indeed, and Unstop job pages."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">32</span> Security: What security practices did you implement?</div>
  <div class="qa-a">"We enforced Manifest V3 Content Security Policy (CSP) on the extension, completely isolated API secrets on the cloud backend, sanitized user inputs to prevent XSS attacks, and implemented strict timeout protections on all external web scraping and API requests."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">33</span> Challenges Faced: What was the single biggest technical challenge you faced?</div>
  <div class="qa-a">"The biggest challenge was the extreme 95.16% to 4.84% class imbalance in the training data. A naive model would simply predict 'legitimate' 100% of the time and get 95% accuracy while catching zero scams. We solved this using balanced class weighting and threshold calibration."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">34</span> Problems During Development: Did you face any API rate-limiting or latency issues?</div>
  <div class="qa-a">"Yes, external API calls to Gemini and search engines initially caused response delays. We resolved this by optimizing parallel requests and implementing graceful fallback mechanisms so that if an external API is slow or quota-limited, the system safely computes an ML-weighted verdict."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">35</span> Solutions to Challenges: How did you calibrate your decision threshold to 0.24?</div>
  <div class="qa-a">"Through 5-fold out-of-fold validation, we plotted precision-recall curves. At the standard 0.50 threshold, scam recall was low because of class imbalance. Calibrating the threshold to 0.24 elevated our scam recall to 81.29% while keeping false alarms at just 1.1%."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">36</span> Limitations: What are the current limitations of ShieldJob AI?</div>
  <div class="qa-a">"Current limitations include requiring an active internet connection for cloud API calls, dependency on external search engine quotas for social verification, and the inability to inspect private encrypted chat groups like Telegram if scammers conduct interviews offline."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">37</span> Future Scope: What enhancements would you build next?</div>
  <div class="qa-a">"In the future, we plan to add automatic DOM scraping in the Chrome extension to highlight scam jobs on web pages without copy-pasting, support multilingual NLP for regional Indian languages, integrate official MCA corporate registry verification, and build a WhatsApp verification bot."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">38</span> Personal Contribution: What was your specific individual contribution?</div>
  <div class="qa-a">"I personally designed and developed the entire pipeline: performing exploratory data analysis, training and tuning the Balanced Random Forest model, engineering Gemini AI prompts, building the BeautifulSoup scraper, developing the Flask web app and Chrome Extension, and deploying on Render."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">39</span> Internship Experience: How did this internship help your technical growth?</div>
  <div class="qa-a">"The internship at VedXlence bridged the gap between academic theory and production software engineering. I gained hands-on experience handling imbalanced ML datasets, integrating modern Generative AI SDKs, building secure browser extensions, and managing cloud deployments."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">40</span> Project Demo Questions: Why does your demo show both ML Confidence and Safety Score?</div>
  <div class="qa-a">"ML Confidence represents the statistical probability output from the Random Forest model alone, while the Safety Score is the final comprehensive 4-pillar aggregated metric. Showing both provides full diagnostic transparency to the user."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">41</span> Diagrams & Screenshots: Why does your architecture use equal 30% weights for ML and AI?</div>
  <div class="qa-a">"We assign 30% to ML for rapid historical pattern matching and 30% to Gemini AI for deep semantic reasoning. Giving them equal weight balances statistical rigor with semantic intelligence, while the remaining 40% is split equally between live website and social footprint verification."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">42</span> Questions About Results: Why is your 98.05% accuracy significant if the baseline is 95.16%?</div>
  <div class="qa-a">"In an imbalanced dataset where 95.16% of samples are legitimate, a useless model that approves everything achieves 95.16% accuracy but has 0% recall on scams. Our model achieves 98.05% accuracy while actively catching 81.29% of all fraud cases, proving genuine predictive power."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">43</span> Challenging Technical Decisions: Why not use a Deep Learning model like LSTM or BERT?</div>
  <div class="qa-a">"While BERT and LSTMs are powerful, they require significant GPU compute resources, high memory footprints, and slow inference times that cause unacceptable latency on free cloud tiers. Random Forest with TF-IDF delivers 98.05% accuracy with sub-millisecond inference and a lightweight 5.6 MB model size."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">44</span> Difficult Reviewer Questions: What if a brand new startup has no website or LinkedIn footprint?</div>
  <div class="qa-a">"Our system handles this gracefully. If a company lacks a website or LinkedIn page, the Website and Social layers return neutral baseline scores, while the ML model and Gemini AI evaluate the job text itself. If the job description is clean and realistic, it receives a Suspicious/Proceed with Caution badge rather than being falsely flagged as Fake."</div>
</div>

<div class="qa-block">
  <div class="qa-q"><span class="q-badge">45</span> Basic Understanding: What is the core difference between Precision and Recall in your project?</div>
  <div class="qa-a">"Recall measures our scam catch rate—out of all real fake jobs, how many did we catch (81.29%). Precision measures our flagging accuracy—when we alert a user that a job is fake, how often are we correct (79.10%). Both are balanced by our F1-score of 80.18%."</div>
</div>

<!-- PART 4 -->
<div class="page-break"></div>
<h1>PART 4 — Questions Specifically Likely to Be Asked (Ranked)</h1>

<h2>🔴 Very High Probability Questions (Must-Prepare)</h2>

<div class="qa-block prob-vh">
  <div class="qa-q">1. What is the 4-layer architecture and what are the exact weights?</div>
  <div class="qa-a">"ShieldJob AI uses four analytical layers: Machine Learning Random Forest at 30%, Google Gemini 2.5 Flash GenAI at 30%, Website Verification at 20%, and Social Media Footprint at 20%. The formula is: <code>Safety Score = 0.30(ML) + 0.30(AI) + 0.20(Web) + 0.20(Social)</code>, mapped to Safe (70-100), Suspicious (50-69), and Fake (0-49)."</div>
</div>

<div class="qa-block prob-vh">
  <div class="qa-q">2. How did you handle the class imbalance in the dataset?</div>
  <div class="qa-a">"The dataset has 17,014 real jobs (95.16%) and only 866 fake jobs (4.84%). We resolved this by using a Balanced Random Forest with <code>class_weight='balanced'</code>, which automatically penalizes misclassifications of minority scam samples inversely proportional to their frequency (~19.6x weight), and calibrated our decision threshold to 0.24."</div>
</div>

<div class="qa-block prob-vh">
  <div class="qa-q">3. Why do you need both Machine Learning and Gemini AI?</div>
  <div class="qa-a">"Machine learning performs fast, low-cost statistical pattern matching on n-grams. Gemini AI provides deep semantic understanding to catch subtle fraud that syntax alone misses—such as disguised registration fee demands or unrealistic salary-to-skill ratios."</div>
</div>

<div class="qa-block prob-vh">
  <div class="qa-q">4. What dataset did you use and what are its key statistics?</div>
  <div class="qa-a">"We used the benchmark EMSCAD dataset from Kaggle containing 17,880 total job postings across 18 features. It has 17,014 legitimate samples (95.16%) and 866 fraudulent samples (4.84%)."</div>
</div>

<div class="qa-block prob-vh">
  <div class="qa-q">5. What are your model's accuracy, precision, and recall numbers?</div>
  <div class="qa-a">"Evaluated via 5-fold stratified cross-validation, the model achieved 98.05% Accuracy, 79.10% Precision, 81.29% Recall (catching 704 out of 866 scams), an 80.18% F1-score, and a 98.49% ROC-AUC."</div>
</div>

<div class="qa-block prob-vh">
  <div class="qa-q">6. How does the Chrome Extension communicate with your system?</div>
  <div class="qa-a">"The Chrome Extension is built on Manifest V3. When a user clicks 'Analyze', the extension sends an HTTPS POST request to our Flask REST endpoint <code>/api/extension/analyze</code> on Render, which processes the multi-layer scan and returns JSON results in under 2 seconds."</div>
</div>

<h2>🟠 High Probability Questions (Commonly Asked)</h2>

<div class="qa-block prob-h">
  <div class="qa-q">7. Why did you choose Random Forest instead of Deep Learning?</div>
  <div class="qa-a">"Random Forest with TF-IDF provides outstanding accuracy (98.05%) with minimal memory usage (5.6 MB model size) and sub-millisecond inference time. Deep learning models like BERT require heavy GPU infrastructure that is impractical for free cloud tiers and real-time browser extension responses."</div>
</div>

<div class="qa-block prob-h">
  <div class="qa-q">8. What features did you extract from the job postings?</div>
  <div class="qa-a">"We concatenated title, company profile, description, requirements, and benefits into a single text corpus and extracted 12,000 unigram and bigram TF-IDF features with sublinear term-frequency scaling."</div>
</div>

<div class="qa-block prob-h">
  <div class="qa-q">9. How do you scrape and verify company websites without getting blocked?</div>
  <div class="qa-a">"We use BeautifulSoup with custom browser User-Agent headers, timeout limits, and domain parsing to extract visible page text, and then pass the content to Gemini AI to assess if it represents active business operations."</div>
</div>

<div class="qa-block prob-h">
  <div class="qa-q">10. What happens if the Gemini API or search quota is exhausted?</div>
  <div class="qa-a">"Our backend implements graceful fallback handlers. If Gemini or search APIs fail, the system automatically recalibrates the safety score using our local Random Forest ML model, ensuring zero server crashes and continuous uptime."</div>
</div>

<div class="qa-block prob-h">
  <div class="qa-q">11. What is the role of the decision threshold 0.24?</div>
  <div class="qa-a">"Due to class imbalance, the standard 0.50 threshold misses too many scams. By setting the threshold to 0.24 through out-of-fold validation, our scam catch rate rose to 81.29% while keeping false alarms to a low 1.1%."</div>
</div>

<div class="qa-block prob-h">
  <div class="qa-q">12. What was your internship organization and duration?</div>
  <div class="qa-a">"I interned at VedXlence Innovations Pvt. Ltd., Hyderabad, for 2 months from May 6, 2026, to July 5, 2026, in the Machine Learning with Python domain."</div>
</div>

<h2>🟡 Possible Questions (Reviewer Dependent)</h2>

<div class="qa-block prob-p">
  <div class="qa-q">13. Which UN Sustainable Development Goals (SDGs) does your project map to?</div>
  <div class="qa-a">"ShieldJob AI maps to SDG 8 (Decent Work and Economic Growth - Target 8.8: protecting labour rights and safe working environments), SDG 9 (Industry, Innovation & Infrastructure), and SDG 16 (Peace, Justice and Strong Institutions - Target 16.4: combating illicit fraud)."</div>
</div>

<div class="qa-block prob-p">
  <div class="qa-q">14. What is sublinear term-frequency scaling in TF-IDF?</div>
  <div class="qa-a">"Sublinear scaling replaces raw term frequency <code>tf</code> with <code>1 + log(tf)</code>. This prevents terms that appear 20 times in a single job posting from having 20 times the weight of a term appearing once, improving classification robustness."</div>
</div>

<div class="qa-block prob-p">
  <div class="qa-q">15. How do you prevent API key leaks in your Chrome Extension?</div>
  <div class="qa-a">"The Chrome Extension contains zero API keys or business secrets. It only sends payloads to our Flask backend on Render, where all external API keys are secured as protected environment variables."</div>
</div>

<!-- PART 5 -->
<div class="page-break"></div>
<h1>PART 5 — Important Points to Memorize (Cheat Facts)</h1>

<table style="width: 100%; font-size: 8.5pt;">
  <tr>
    <th style="width: 28%;">Parameter / Category</th>
    <th>Exact Verified Fact (From PPT & Report)</th>
  </tr>
  <tr>
    <td><strong>Candidate Details</strong></td>
    <td>Tanuku Ram Sai | PIN: 24A95A0503 | Dept. of CSE, Aditya University, Surampalem</td>
  </tr>
  <tr>
    <td><strong>Internship Organization</strong></td>
    <td>VedXlence Innovations Pvt. Ltd., Hyderabad, Telangana, India (https://www.vedxlence.in/)</td>
  </tr>
  <tr>
    <td><strong>Internship Duration & Domain</strong></td>
    <td>2 Months (May 6, 2026 – July 5, 2026) | Domain: Machine Learning with Python</td>
  </tr>
  <tr>
    <td><strong>Project Guide & HOD</strong></td>
    <td>Guide: Mr. M. Srinu, Asst. Professor | HOD: Dr. T. Sudha Rani, Professor & Head, Dept. of CSE</td>
  </tr>
  <tr>
    <td><strong>Project Title</strong></td>
    <td>ShieldJob AI: Multi-Modal Fake Job Detection System</td>
  </tr>
  <tr>
    <td><strong>Dataset & Sample Count</strong></td>
    <td>EMSCAD / Kaggle Fake Job Postings: 17,880 Total (17,014 Legitimate / 95.16% vs 866 Fraudulent / 4.84%)</td>
  </tr>
  <tr>
    <td><strong>NLP / Feature Extraction</strong></td>
    <td>TfidfVectorizer: max_features=12,000, ngram_range=(1,2), sublinear_tf=True, min_df=2</td>
  </tr>
  <tr>
    <td><strong>ML Model & Hyperparameters</strong></td>
    <td>RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42), Threshold = 0.24</td>
  </tr>
  <tr>
    <td><strong>Generative AI Model</strong></td>
    <td>Google Gemini 2.5 Flash via <code>google-generativeai</code> SDK</td>
  </tr>
  <tr>
    <td><strong>4-Pillar Scoring Formula</strong></td>
    <td><code>Safety Score = 0.30(ML) + 0.30(AI) + 0.20(Website) + 0.20(Social)</code></td>
  </tr>
  <tr>
    <td><strong>Score Categories & Badges</strong></td>
    <td>70–100: Legitimate (Emerald) | 50–69: Suspicious (Amber) | 0–49: Likely Fake (Rose/Red)</td>
  </tr>
  <tr>
    <td><strong>Verified Accuracy & Metrics</strong></td>
    <td>Accuracy: 98.05% | Precision: 79.10% | Recall: 81.29% | F1-Score: 80.18% | ROC-AUC: 98.49%</td>
  </tr>
  <tr>
    <td><strong>Confusion Matrix Values</strong></td>
    <td>TN: 16,828 (98.9%) | FP: 186 (1.1%) | FN: 162 (18.7%) | TP: 704 (81.3% scams caught)</td>
  </tr>
  <tr>
    <td><strong>Web & Browser Tech Stack</strong></td>
    <td>Python 3.11, Flask REST API, Gunicorn, HTML5, Vanilla CSS3 Glassmorphism, JS ES6, Chrome MV3</td>
  </tr>
  <tr>
    <td><strong>Live Cloud URL & Repo</strong></td>
    <td>Live App: <code>https://fake-job-detection-iuxn.onrender.com/#analyzer</code> | GitHub: <code>Coder-sai2004/Fake_Job_Detection</code></td>
  </tr>
  <tr>
    <td><strong>UN SDG Mappings</strong></td>
    <td>SDG 8 (Decent Work & Economic Growth - Target 8.8), SDG 9 (Innovation), SDG 16 (Target 16.4)</td>
  </tr>
</table>

<!-- PART 6 -->
<div class="page-break"></div>
<h1>PART 6 — Possible Tricky Questions & Honest Spoken Answers</h1>

<div class="qa-block">
  <div class="qa-q">Q1: Why did you choose Random Forest instead of XGBoost or a Transformer model?</div>
  <div class="qa-a">"While XGBoost and Transformers are powerful, Random Forest was selected because it naturally handles high-dimensional sparse text vectors, provides built-in balanced class weighting without extreme hyperparameter sensitivity, trains in seconds, and serializes to a lightweight 5.6 MB file that runs with sub-millisecond latency on cloud servers."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q2: Why use both classical ML and Gemini AI? Isn't Gemini alone enough?</div>
  <div class="qa-a">"Relying solely on Gemini AI would introduce significant API latency, recurring financial costs, and vulnerability to network rate limits. Classical ML provides a fast, zero-cost first line of statistical defense, while Gemini provides high-level semantic reasoning for nuanced fraud. Together, they create a robust, cost-effective hybrid system."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q3: How do you know your model is not overfitting?</div>
  <div class="qa-a">"We validated the model using 5-Fold Stratified Out-of-Fold Cross-Validation across all 17,880 samples, ensuring evaluation was always performed on unseen data. Additionally, our ensemble of 100 decorrelated trees and a minimum document frequency constraint (min_df=2) prevents individual noisy words from overfitting."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q4: What happens if the Gemini AI gives an incorrect response or hallucinates?</div>
  <div class="qa-a">"Gemini AI contributes only 30% of the overall score and is constrained with strict system prompts and JSON schema outputs. Even if the LLM output is imperfect, the remaining 70%—comprising our Random Forest model, website domain scraping, and social footprint verification—counterbalances the assessment."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q5: What happens if a legitimate new startup has no company website or LinkedIn page?</div>
  <div class="qa-a">"When website or social data is unavailable, those modules return neutral baseline scores. The system relies primarily on the job text evaluated by ML and Gemini. If the description has realistic compensation and no fee demands, it receives a 'Suspicious / Proceed with Caution' badge rather than being falsely classified as a fake scam."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q6: What happens when the input text is completely different from your training data?</div>
  <div class="qa-a">"If novel vocabulary appears, the TF-IDF vectorizer captures available token overlaps, but our Gemini AI layer steps in to understand the semantic context and meaning. Because Gemini is a general-purpose LLM, it evaluates the logical coherence and scam indicators regardless of unseen vocabulary."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q7: What is the most difficult part of the project that you personally implemented?</div>
  <div class="qa-a">"The most challenging aspect was architecting the multi-modal score aggregation engine and handling class imbalance. Calibrating the decision threshold to 0.24 through cross-validation and building seamless API fallback mechanisms required deep debugging to ensure high scam recall without sacrificing speed."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q8: Why should someone trust your system over their own judgment?</div>
  <div class="qa-a">"ShieldJob AI performs multi-dimensional checks that a human cannot easily do in a few seconds—such as calculating n-gram probability against 17,880 historical patterns, analyzing domain metadata, and checking cross-platform complaints simultaneously—and provides transparent explainability bullets to help the user make an informed decision."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q9: What are the security concerns regarding your Chrome Extension?</div>
  <div class="qa-a">"The Chrome Extension is built strictly under Manifest V3, adhering to modern Content Security Policies. It does not store or process user passwords or personal browsing history, and communicates only with our secured HTTPS backend endpoint on Render."</div>
</div>

<div class="qa-block">
  <div class="qa-q">Q10: How can the project be scaled for millions of users?</div>
  <div class="qa-a">"To scale, the Flask microservice can be containerized using Docker and deployed on an autoscaling Kubernetes cluster behind an Nginx load balancer, with Redis caching for frequently queried job postings and company domains."</div>
</div>

<!-- PART 7 -->
<div class="page-break"></div>
<h1>PART 7 — PPT / Report Consistency Check Table</h1>
<p><em>This comparison verifies all project facts between the Presentation PPT and the Internship Report to ensure you never make contradictory statements during review.</em></p>

<table>
  <tr>
    <th style="width: 22%;">Issue / Parameter</th>
    <th style="width: 26%;">PPT Claim</th>
    <th style="width: 26%;">Report Claim</th>
    <th style="width: 26%;">What You Should Speak</th>
  </tr>
  <tr>
    <td><strong>Internship Company</strong></td>
    <td>Not explicitly named on slide titles (focuses on Aditya University)</td>
    <td>VedXlence Innovations Pvt. Ltd., Hyderabad (AICTE Certified)</td>
    <td><strong>Speak:</strong> "Carried out at VedXlence Innovations Pvt. Ltd., Hyderabad."</td>
  </tr>
  <tr>
    <td><strong>Internship Dates</strong></td>
    <td>Academic Year 2025–2026</td>
    <td>May 6, 2026 – July 5, 2026 (2 Months)</td>
    <td><strong>Speak:</strong> "2-month internship from May 6, 2026 to July 5, 2026."</td>
  </tr>
  <tr>
    <td><strong>Gemini Model Version</strong></td>
    <td>"Google Gemini AI"</td>
    <td>"Google Gemini 2.5 Flash"</td>
    <td><strong>Speak:</strong> "Google Gemini 2.5 Flash via official Python SDK."</td>
  </tr>
  <tr>
    <td><strong>Scoring Weights</strong></td>
    <td>30% ML, 30% Gemini AI, 20% Website, 20% Social</td>
    <td>30% ML, 30% Gemini AI, 20% Website, 20% Social</td>
    <td><strong>Consistent:</strong> Use 30% ML, 30% AI, 20% Web, 20% Social.</td>
  </tr>
  <tr>
    <td><strong>Score Categories</strong></td>
    <td>Legitimate (Safe), Suspicious, Likely Fake</td>
    <td>Safe (&ge;70), Suspicious (50–69), Likely Fake (&lt;50)</td>
    <td><strong>Consistent:</strong> Use 70–100 Safe, 50–69 Suspicious, 0–49 Fake.</td>
  </tr>
  <tr>
    <td><strong>Dataset Size & Source</strong></td>
    <td>17,880 benchmark job postings (EMSCAD)</td>
    <td>17,880 postings (17,014 real / 866 fake) from EMSCAD / Kaggle</td>
    <td><strong>Consistent:</strong> 17,880 samples (95.16% real, 4.84% fake).</td>
  </tr>
  <tr>
    <td><strong>Model & Hyperparams</strong></td>
    <td>Random Forest + TF-IDF</td>
    <td>Balanced Random Forest (n_estimators=100, class_weight='balanced', threshold=0.24, max_features=12,000)</td>
    <td><strong>Speak:</strong> Balanced Random Forest with 100 trees, 12K TF-IDF features.</td>
  </tr>
  <tr>
    <td><strong>Evaluation Metrics</strong></td>
    <td>Accuracy: 98.05%, Recall: 81.29%, Precision: 79.10%, ROC-AUC: 98.49%</td>
    <td>Accuracy: 98.05%, Precision: 79.10%, Recall: 81.29%, F1: 80.18%, ROC-AUC: 98.49%</td>
    <td><strong>Consistent:</strong> State exact metrics confirmed by both documents.</td>
  </tr>
  <tr>
    <td><strong>Confusion Matrix</strong></td>
    <td>16,828 approved, 704 scams caught, 186 false alarms</td>
    <td>TN: 16,828, FP: 186, FN: 162, TP: 704 (5-fold out-of-fold)</td>
    <td><strong>Consistent:</strong> Cite 16,828 TN, 704 TP, 186 FP, 162 FN.</td>
  </tr>
  <tr>
    <td><strong>Web Scraping Tool</strong></td>
    <td>"SerpAPI & Google Custom Search"</td>
    <td>"BeautifulSoup DOM scraper + Brave Search / Google CSE"</td>
    <td><strong>Speak:</strong> "BeautifulSoup for website scraping, Brave Search/Google CSE for social auditing."</td>
  </tr>
  <tr>
    <td><strong>Chrome Extension</strong></td>
    <td>Manifest V3 Chrome Extension</td>
    <td>Manifest V3 Chrome Extension (packaged in fake-job-detector-extension/)</td>
    <td><strong>Consistent:</strong> Chrome Extension built on Manifest V3.</td>
  </tr>
  <tr>
    <td><strong>Cloud Hosting</strong></td>
    <td>Render Platform</td>
    <td>Render Platform (https://fake-job-detection-iuxn.onrender.com/#analyzer)</td>
    <td><strong>Consistent:</strong> Render Cloud Platform.</td>
  </tr>
</table>

<!-- PART 8 -->
<div class="page-break"></div>
<h1>PART 8 — Final Review Cheat Sheet (Read Before Entering)</h1>

<div class="info-card">
  <strong>Project in One Sentence:</strong> ShieldJob AI is a multi-modal fake job detection platform combining Balanced Random Forest ML (30%), Google Gemini 2.5 Flash (30%), BeautifulSoup website scraping (20%), and live social media auditing (20%) to deliver 0–100 safety scores via a Flask web app and Chrome Extension.
</div>

<div class="grid-2">
  <div class="info-card">
    <strong>Problem:</strong> Rapid rise of recruitment fraud, fee extortion, and company impersonation on LinkedIn/Naukri where single-layer checks fail.
  </div>
  <div class="info-card">
    <strong>Solution:</strong> A 4-pillar verification ecosystem that cross-checks job text, semantic red flags, domain legitimacy, and social presence.
  </div>
</div>

<div class="grid-2">
  <div class="success-card">
    <strong>Technologies:</strong> Python 3.11, Flask, Scikit-Learn, Gemini 2.5 Flash, BeautifulSoup, HTML5, Vanilla CSS3, JS ES6, Chrome MV3, Render.
  </div>
  <div class="success-card">
    <strong>ML / NLP Specs:</strong> 17,880 EMSCAD samples, TF-IDF (12K features, unigrams+bigrams, sublinear_tf), Balanced Random Forest (100 trees, threshold 0.24).
  </div>
</div>

<div class="grid-2">
  <div class="warning-card">
    <strong>Key Results:</strong> 98.05% Accuracy, 79.10% Precision, 81.29% Recall (704 scams caught), 80.18% F1, 98.49% ROC-AUC.
  </div>
  <div class="warning-card">
    <strong>Challenges & Solutions:</strong> Class imbalance (4.84% scams) solved via balanced class weighting and threshold calibration (0.24); API latency solved via parallel requests and fallbacks.
  </div>
</div>

<div class="info-card">
  <strong>My Contribution:</strong> End-to-end dataset preprocessing, ML model training & threshold tuning, Gemini API integration, website scraper, Flask web app, Manifest V3 Chrome Extension, and Render cloud deployment.
</div>

<div class="grid-2">
  <div class="info-card">
    <strong>Limitations:</strong> Requires internet for API calls; external search API quotas; cannot inspect private Telegram chats.
  </div>
  <div class="info-card">
    <strong>Future Scope:</strong> Automatic DOM scraping without copy-paste; multilingual NLP; MCA registry verification; WhatsApp bot.
  </div>
</div>

<h2>Top 10 Questions You Must Know By Heart</h2>
<ol style="font-size: 8.5pt; line-height: 1.5; padding-left: 18px; margin-top: 4px;">
  <li><strong>What is the scoring formula?</strong> <code>Safety Score = 0.30*ML + 0.30*AI + 0.20*Website + 0.20*Social</code>. Badges: &ge;70 Safe, 50–69 Suspicious, &lt;50 Fake.</li>
  <li><strong>How did you solve class imbalance?</strong> Used <code>class_weight='balanced'</code> in Random Forest (giving ~19.6x weight to scam class) and calibrated threshold to 0.24.</li>
  <li><strong>Why use both ML and Gemini AI?</strong> ML gives fast statistical pattern matching on n-grams; Gemini gives contextual reasoning to catch covert fee demands and subtle fraud.</li>
  <li><strong>What are your verified results?</strong> 98.05% Accuracy, 79.10% Precision, 81.29% Recall, 80.18% F1-Score, 98.49% ROC-AUC on 17,880 samples.</li>
  <li><strong>What dataset did you use?</strong> EMSCAD (17,880 job postings: 17,014 real vs 866 fake) with 5-fold stratified cross-validation.</li>
  <li><strong>Why did you choose TF-IDF with (1,2) n-grams?</strong> Unigrams capture single words; bigrams capture critical phrases like 'wire transfer' and 'training fee'. Sublinear TF prevents high-frequency dominance.</li>
  <li><strong>Where did you intern and for how long?</strong> VedXlence Innovations Pvt. Ltd., Hyderabad | 2 Months (May 6, 2026 – July 5, 2026) | Domain: Machine Learning with Python.</li>
  <li><strong>How does the Chrome Extension work?</strong> Built on Manifest V3; sends job text via HTTPS to Flask REST API <code>/api/extension/analyze</code> and displays score & badges in under 2 seconds.</li>
  <li><strong>Where is it deployed?</strong> Backend on Render Cloud (<code>https://fake-job-detection-iuxn.onrender.com/#analyzer</code>) with Gunicorn WSGI.</li>
  <li><strong>What is the difference between Precision and Recall in your model?</strong> Recall is scam catch rate (81.29% / 704 caught); Precision is alarm accuracy (79.10% of flags are real scams).</li>
</ol>

</body>
</html>
"""

# Save HTML file
html_path = os.path.abspath('ShieldJob_AI_Internship_Review_Preparation_Guide.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'HTML written to {html_path}')

# Output PDF paths
pdf_path_1 = os.path.abspath('ShieldJob_AI_Internship_Review_Preparation_Guide.pdf')
pdf_path_2 = r'C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\ShieldJob_AI_Internship_Review_Preparation_Guide.pdf'

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_path_1}',
    '--no-pdf-header-footer',
    html_path
]

print('Running Chrome headless to generate PDF...')
subprocess.run(cmd, check=True)
print(f'PDF generated successfully at {pdf_path_1} (Size: {os.path.getsize(pdf_path_1)} bytes)')

# Copy to internship directory as well
import shutil
shutil.copy2(pdf_path_1, pdf_path_2)
print(f'PDF copied to internship directory: {pdf_path_2} (Size: {os.path.getsize(pdf_path_2)} bytes)')
