/**
 * ShieldJob AI — Chrome Extension Popup Script
 *
 * Architecture:
 *  - Single responsibility: send job description to backend, render result.
 *  - All state lives in the DOM views (input / loading / result / error).
 *  - No framework — pure vanilla JS for minimum footprint.
 *  - Structured for easy future extension (e.g. content-script auto-fill).
 */

'use strict';

// ============================================================
// Constants
// ============================================================

const API_URL = 'https://fake-job-detection-iuxn.onrender.com/api/extension/analyze';
const WEBSITE_URL = 'https://fake-job-detection-iuxn.onrender.com/';
const REQUEST_TIMEOUT_MS = 60_000; // 60 s — Render cold-starts can be slow

const LOADING_STEPS = [
  'Checking job description…',
  'Running ML classifier…',
  'Validating with Gemini AI…',
  'Calculating risk score…',
];

// ============================================================
// DOM References
// ============================================================

const views = {
  input: document.getElementById('viewInput'),
  loading: document.getElementById('viewLoading'),
  result: document.getElementById('viewResult'),
  error: document.getElementById('viewError'),
};

const els = {
  // Header
  statusBadge: document.getElementById('statusBadge'),

  // Input view
  jobDescription: document.getElementById('jobDescription'),
  charCounter: document.getElementById('charCounter'),
  analyzeBtn: document.getElementById('analyzeBtn'),
  inputError: document.getElementById('inputError'),
  inputErrorMsg: document.getElementById('inputErrorMsg'),

  // Loading view
  loadingStep: document.getElementById('loadingStep'),
  stepDots: document.querySelectorAll('.step-dot'),

  // Result view
  verdictBanner: document.getElementById('verdictBanner'),
  verdictIcon: document.getElementById('verdictIcon'),
  verdictLabel: document.getElementById('verdictLabel'),
  verdictSublabel: document.getElementById('verdictSublabel'),
  verdictScoreNum: document.getElementById('verdictScoreNum'),
  riskBarFill: document.getElementById('riskBarFill'),
  riskBarTrack: document.getElementById('riskBarTrack'),
  riskLevelLabel: document.getElementById('riskLevelLabel'),
  confidenceValue: document.getElementById('confidenceValue'),
  confidenceRow: document.getElementById('confidenceRow'),
  aiNotice: document.getElementById('aiNotice'),
  reasonsList: document.getElementById('reasonsList'),
  viewFullBtn: document.getElementById('viewFullBtn'),
  retryBtn: document.getElementById('retryBtn'),

  // Error view
  errorTitle: document.getElementById('errorTitle'),
  errorMessage: document.getElementById('errorMessage'),
  errorRetryBtn: document.getElementById('errorRetryBtn'),
  errorOpenWebBtn: document.getElementById('errorOpenWebBtn'),

  // Footer
  footerOpenWebBtn: document.getElementById('footerOpenWebBtn'),
};

// ============================================================
// View Management
// ============================================================

function showView(name) {
  Object.entries(views).forEach(([key, el]) => {
    el.classList.toggle('active', key === name);
  });
}

// ============================================================
// Header Badge
// ============================================================

function setBadge(text, cls = '') {
  els.statusBadge.textContent = text;
  els.statusBadge.className = 'header-badge' + (cls ? ' ' + cls : '');
}

// ============================================================
// Character Counter
// ============================================================

els.jobDescription.addEventListener('input', () => {
  const len = els.jobDescription.value.length;
  els.charCounter.textContent = `${len.toLocaleString()} characters`;
  els.charCounter.className = 'char-counter' + (len > 0 && len < 50 ? ' warn' : '');

  // Clear inline error when user starts typing
  if (len > 0) hideInputError();
});

// ============================================================
// Inline Input Error
// ============================================================

function showInputError(msg) {
  els.inputErrorMsg.textContent = msg;
  els.inputError.hidden = false;
}

function hideInputError() {
  els.inputError.hidden = true;
}

// ============================================================
// Loading Animation
// ============================================================

let loadingTimer = null;
let stepIndex = 0;

function startLoadingAnimation() {
  stepIndex = 0;
  updateLoadingStep();
  loadingTimer = setInterval(() => {
    stepIndex = (stepIndex + 1) % LOADING_STEPS.length;
    updateLoadingStep();
  }, 2800);
}

function stopLoadingAnimation() {
  clearInterval(loadingTimer);
  loadingTimer = null;
}

function updateLoadingStep() {
  els.loadingStep.textContent = LOADING_STEPS[stepIndex];
  els.stepDots.forEach((dot, i) => {
    dot.classList.toggle('active', i === stepIndex);
  });
}

// ============================================================
// Result Rendering
// ============================================================

/**
 * Map backend verdict → display properties.
 * Handles all 3 possible verdict strings from the backend.
 */
function getVerdictMeta(verdict) {
  const v = (verdict || '').toLowerCase();

  if (v.includes('real')) {
    return {
      cssClass: 'real',
      icon: '✅',
      label: 'LEGITIMATE JOB',
      sublabel: 'Looks like a real job posting',
      riskClass: 'low',
      badgeCls: 'low',
    };
  }
  if (v.includes('suspicious')) {
    return {
      cssClass: 'sus',
      icon: '⚠️',
      label: 'SUSPICIOUS',
      sublabel: 'Proceed with caution — verify independently',
      riskClass: 'medium',
      badgeCls: 'medium',
    };
  }
  // Default: fake
  return {
    cssClass: 'fake',
    icon: '🚨',
    label: 'LIKELY FAKE',
    sublabel: 'High risk — do not share personal info',
    riskClass: 'high',
    badgeCls: 'high',
  };
}

function renderResult(data) {
  const meta = getVerdictMeta(data.verdict);

  // Verdict banner
  els.verdictBanner.className = `verdict-banner ${meta.cssClass}`;
  els.verdictIcon.textContent = meta.icon;
  els.verdictLabel.textContent = meta.label;
  els.verdictSublabel.textContent = meta.sublabel;

  // Risk score circle
  const score = Math.min(100, Math.max(0, data.risk_score ?? 0));
  els.verdictScoreNum.textContent = score;

  // Risk bar
  const riskClass = (data.risk_level || meta.riskClass).toLowerCase();
  els.riskBarFill.className = `risk-bar-fill ${riskClass}`;
  els.riskBarTrack.setAttribute('aria-valuenow', score);
  // Animate bar after short delay so CSS transition fires
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      els.riskBarFill.style.width = `${score}%`;
    });
  });

  // Risk level badge
  const levelText = data.risk_level || (riskClass.charAt(0).toUpperCase() + riskClass.slice(1));
  els.riskLevelLabel.textContent = levelText;
  els.riskLevelLabel.className = `risk-level-badge ${riskClass}`;

  // Confidence
  if (data.confidence != null) {
    els.confidenceValue.textContent = `${data.confidence}%`;
    els.confidenceRow.hidden = false;
  } else {
    els.confidenceRow.hidden = true;
  }

  // AI unavailable notice
  els.aiNotice.hidden = !data.ai_unavailable;

  // Reasons
  els.reasonsList.innerHTML = '';
  const reasons = Array.isArray(data.reasons) ? data.reasons : [];
  if (reasons.length > 0) {
    reasons.slice(0, 5).forEach(reason => {
      const li = document.createElement('li');
      li.textContent = reason;
      els.reasonsList.appendChild(li);
    });
    document.getElementById('reasonsSection').hidden = false;
  } else {
    document.getElementById('reasonsSection').hidden = true;
  }

  showView('result');
  setBadge('Done');
}

// ============================================================
// Open Website
// ============================================================

function openWebsite() {
  chrome.tabs.create({ url: WEBSITE_URL });
}

// ============================================================
// Error Rendering
// ============================================================

const ERROR_MESSAGES = {
  INVALID_INPUT: '⚠️ Please paste a job description (at least 20 characters).',
  NOT_A_JOB: '⚠️ The pasted text does not look like a job description. Please paste a real job posting.',
  TIMEOUT: '⚠️ Analysis is taking too long. The server may be starting up — please try again in 30 seconds.',
  NETWORK: '⚠️ Network error. Please check your internet connection and try again.',
  INTERNAL_ERROR: '⚠️ The server encountered an error. Please try again.',
  DEFAULT: '⚠️ Unable to analyze the job. Please try again.',
};

function renderError(code, customMessage) {
  const msg = customMessage
    || ERROR_MESSAGES[code]
    || ERROR_MESSAGES.DEFAULT;

  els.errorTitle.textContent = 'Analysis Failed';
  els.errorMessage.textContent = msg.replace(/^⚠️\s*/, '');

  showView('error');
  setBadge('Error');
}

// ============================================================
// API Call
// ============================================================

async function analyzeJob(jobDescription) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_description: jobDescription }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    const data = await response.json();

    if (!response.ok) {
      // Backend returned a structured error
      renderError(data.code, data.error ? `⚠️ ${data.error}` : null);
      return;
    }

    renderResult(data);

  } catch (err) {
    clearTimeout(timeoutId);

    if (err.name === 'AbortError') {
      renderError('TIMEOUT');
    } else {
      console.error('[ShieldJob Extension] Fetch error:', err);
      renderError('NETWORK');
    }
  } finally {
    stopLoadingAnimation();
    setBadge(views.error.classList.contains('active') ? 'Error' : 'Done');
  }
}

// ============================================================
// Analyze Button Handler
// ============================================================

function handleAnalyze() {
  hideInputError();

  const text = els.jobDescription.value.trim();

  if (!text) {
    showInputError('Please paste a job description first.');
    els.jobDescription.focus();
    return;
  }

  if (text.length < 20) {
    showInputError('Description is too short. Please paste a complete job posting.');
    els.jobDescription.focus();
    return;
  }

  // Switch to loading
  showView('loading');
  setBadge('Scanning…', 'scanning');
  startLoadingAnimation();

  // Kick off API call
  analyzeJob(text);
}

// ============================================================
// Retry / Reset
// ============================================================

function handleRetry() {
  hideInputError();
  showView('input');
  setBadge('Ready');
  els.jobDescription.focus();
}

// ============================================================
// Event Listeners
// ============================================================

els.analyzeBtn.addEventListener('click', handleAnalyze);

// Allow Ctrl+Enter to trigger analysis
els.jobDescription.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    handleAnalyze();
  }
});

els.retryBtn.addEventListener('click', handleRetry);
els.errorRetryBtn.addEventListener('click', handleRetry);
els.errorOpenWebBtn.addEventListener('click', openWebsite);
els.viewFullBtn.addEventListener('click', openWebsite);
els.footerOpenWebBtn.addEventListener('click', openWebsite);
