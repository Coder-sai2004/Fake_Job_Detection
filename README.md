# 🛡️ Fake Job Detection System

An AI-powered web application that helps users identify fraudulent job postings by combining Machine Learning, Generative AI analysis, Website Reputation Analysis, and Company Social Presence Verification.

---

## 📌 Project Overview

Fake job scams have become increasingly common on job portals and social media platforms. This project aims to protect job seekers by analyzing job descriptions and company information to determine whether a job posting is:

- ✅ Legitimate
- ⚠️ Suspicious
- ❌ Fake Job

The system combines multiple detection techniques to provide a comprehensive legitimacy score.

---

## 🚀 Features

### 1. Machine Learning Detection
- Predicts legitimacy of job postings using a trained ML model.
- Generates an ML confidence score.

### 2. AI Content Validation
- Uses Google Gemini AI to analyze:
  - Job content quality
  - Scam indicators
  - Professionalism
  - Recruitment authenticity

### 3. Website Analysis
- Evaluates the company's website.
- Checks:
  - Domain credibility
  - Security indicators
  - Professional appearance
  - Trust signals

### 4. Social Media Analysis
- Examines:
  - LinkedIn presence
  - Online visibility
  - Community discussions
  - Scam reports

### 5. Comprehensive Risk Assessment
- Combines:
  - ML Score
  - AI Score
  - Website Score
  - Social Score

- Produces:
  - Final Legitimacy Score
  - Risk Level
  - Detailed Explanation

---

## 🏗️ System Architecture

```text
User Input
     │
     ▼
Job Description
     │
     ├────────────► ML Model
     │
     ├────────────► Gemini AI Validation
     │
     ├────────────► Website Analyzer
     │
     └────────────► Social Media Analyzer
                    │
                    ▼
            Score Aggregation
                    │
                    ▼
             Final Prediction"# Fake_Job_Detection" 
