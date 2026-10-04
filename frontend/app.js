
let currentAnalysisData = null;

function renderResults(data) {
    currentAnalysisData = data;
    const container = document.getElementById('resultsContainer');
    const warningContainer = document.getElementById('aiWarningContainer');
    if (!container) return;

    if (warningContainer) {
        if (data.ai_unavailable) {
            warningContainer.innerHTML = `
                <div class="ai-warning-banner" id="aiWarningBanner">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <div class="ai-warning-text">
                        <strong>AI Assistant is Busy</strong>
                        <span>${escapeHtml(data.ai_error_message || 'Rate limit reached.')} The Machine Learning score below is still fully active and accurate.</span>
                    </div>
                    <button class="ai-warning-close" onclick="this.parentElement.style.display='none'" aria-label="Dismiss">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            `;
        } else {
            warningContainer.innerHTML = '';
        }
    }

    const prediction = data.prediction || 'Unknown';
    const finalScore = (data.final_score !== undefined && data.final_score !== null) ? data.final_score : 50;
    const mlScore = (data.ml_score !== undefined && data.ml_score !== null) ? data.ml_score : 50;
    const aiScore = (data.ai_score !== undefined && data.ai_score !== null) ? data.ai_score : 50;
    const websiteScore = (data.website_score !== undefined && data.website_score !== null) ? data.website_score : 50;
    const socialScore = (data.social_score !== undefined && data.social_score !== null) ? data.social_score : 50;
    const riskLevel = data.risk_level || 'Medium';
    const reasons = data.reasons || [];
    const websiteAnalysis = data.website_analysis;
    const socialAnalysis = data.social_analysis;

    let cardClass = 'verdict-fake';
    let badgeHtml = '<i class="fa-solid fa-circle-xmark"></i><span>HIGH RISK — LIKELY A SCAM</span>';
    let headline = 'Warning! This posting has strong red flags of an employment scam.';

    if (prediction === 'Real Job') {
        cardClass = 'verdict-real';
        badgeHtml = '<i class="fa-solid fa-circle-check"></i><span>LOOKS LEGITIMATE — SAFE TO APPLY</span>';
        headline = 'This job posting matches verified hiring standards.';
    } else if (prediction === 'Suspicious Job') {
        cardClass = 'verdict-suspicious';
        badgeHtml = '<i class="fa-solid fa-triangle-exclamation"></i><span>SUSPICIOUS — PROCEED WITH CAUTION</span>';
        headline = 'We found mixed signals. Do not pay any money or share sensitive IDs.';
    }

    const strokeDashoffset = (326.72 - (326.72 * finalScore) / 100).toFixed(2);
    const aiBarClass = data.ai_unavailable ? 'bar-muted' : '';
    const aiScoreTag = data.ai_unavailable ? '<span class="unavail-tag">est.</span>' : '';
    const aiFooterText = data.ai_unavailable ? 'AI Busy — Estimated' : 'AI Tone &amp; Offer Audit';

    let socialFooterText = 'Online Employer Presence';
    let socialVerificationTag = '<span class="unverified-tag"><i class="fa-solid fa-circle-question"></i> Unverified</span>';

    if (socialAnalysis) {
        const method = socialAnalysis.verification_method || '';
        if (method.includes('real_search') || method === 'google_cse') {
            socialFooterText = 'Live Search Verified';
            socialVerificationTag = '<span class="verified-tag"><i class="fa-solid fa-magnifying-glass"></i> Live Search</span>';
        } else if (method === 'ai_knowledge') {
            socialFooterText = 'Verified via AI Knowledge';
            socialVerificationTag = '<span class="verified-tag" style="background: rgba(99, 102, 241, 0.15); color: #A5B4FC; border-color: rgba(99, 102, 241, 0.4);"><i class="fa-solid fa-brain"></i> AI Knowledge</span>';
        }
    }

    let reasonsHtml = '';
    if (reasons.length > 0) {
        reasonsHtml = reasons.map(r => `
            <div class="reason-bullet">
                <i class="fa-solid fa-triangle-exclamation bullet-icon"></i>
                <span>${escapeHtml(r)}</span>
            </div>
        `).join('');
    } else {
        reasonsHtml = `
            <div class="reason-bullet reason-bullet-ok">
                <i class="fa-solid fa-circle-check bullet-icon"></i>
                <span>No major scam red flags or high-risk language detected in this posting.</span>
            </div>
        `;
    }

    let websiteHtml = '';
    if (websiteAnalysis) {
        const webRisk = (websiteAnalysis.risk_level || 'Medium').toLowerCase();
        const webAiNote = websiteAnalysis.ai_unavailable
            ? '<span class="intel-sub"><i class="fa-solid fa-circle-exclamation"></i> Heuristic Check (AI Busy)</span>'
            : '';
        websiteHtml = `
            <div class="intel-card">
                <div class="intel-header">
                    <div class="intel-header-left">
                        <i class="fa-solid fa-globe intel-icon"></i>
                        <div>
                            <span class="intel-title">Company Website Audit</span>
                            <span class="risk-badge risk-${webRisk}">${escapeHtml(websiteAnalysis.risk_level || 'Medium')} Risk</span>
                        </div>
                    </div>
                    <div class="intel-header-right">
                        <span class="intel-score-tag">${websiteScore}/100</span>
                        ${webAiNote}
                    </div>
                </div>
                <div class="intel-body">
                    <p class="intel-summary">${escapeHtml(websiteAnalysis.summary || '')}</p>
                </div>
            </div>
        `;
    }

    let socialHtml = '';
    if (socialAnalysis) {
        let evidenceContent = '';
        if (socialAnalysis.evidence) {
            const ev = socialAnalysis.evidence;
            const liStatus = (ev.linkedin && ev.linkedin.status) || 'Unknown';
            const liClass = (liStatus === 'Found' || liStatus === 'Likely Present') ? 'evidence-found' : (liStatus === 'Not Found' ? 'evidence-notfound' : 'evidence-unknown');

            const rdStatus = (ev.reddit && ev.reddit.status) || 'Unknown';
            const rdClass = (rdStatus === 'Found') ? 'evidence-found' : (rdStatus === 'Not Found' ? 'evidence-notfound' : 'evidence-unknown');
            const rdCountText = (rdStatus === 'Found' && ev.reddit.count) ? ` (${ev.reddit.count} discussion${ev.reddit.count !== 1 ? 's' : ''})` : '';

            const rvStatus = (ev.reviews && ev.reviews.status) || 'Unknown';
            const rvClass = (rvStatus === 'Found' || rvStatus === 'Likely Present') ? 'evidence-found' : (rvStatus === 'Not Found' ? 'evidence-notfound' : 'evidence-unknown');
            const rvCountText = (rvStatus === 'Found' && ev.reviews.count) ? ` (${ev.reviews.count} platform${ev.reviews.count !== 1 ? 's' : ''})` : '';

            const scamSignals = ev.scam_signals || [];
            const scamClass = (scamSignals.length > 0) ? 'evidence-warning' : 'evidence-found';
            const scamText = (scamSignals.length > 0) ? `${scamSignals.length} reported` : 'None found';

            let searchUrlsHtml = '';
            if (ev.search_results && ev.search_results.length > 0) {
                searchUrlsHtml = `
                    <div class="evidence-urls">
                        <span class="evidence-urls-label">Search Evidence:</span>
                        ${ev.search_results.slice(0, 3).map(res => `
                            <a href="${escapeHtml(res.url)}" target="_blank" rel="noopener noreferrer" class="evidence-url-link">
                                <i class="fa-solid fa-arrow-up-right-from-square"></i>
                                ${escapeHtml(res.title ? res.title.slice(0, 55) + (res.title.length > 55 ? '...' : '') : 'Link')}
                            </a>
                        `).join('')}
                    </div>
                `;
            }

            let aiSummaryHtml = '';
            if (socialAnalysis.ai_summary) {
                aiSummaryHtml = `
                    <p class="intel-summary social-ai-summary">
                        <i class="fa-solid fa-circle-info social-summary-icon"></i>
                        ${escapeHtml(socialAnalysis.ai_summary)}
                    </p>
                `;
            }

            evidenceContent = `
                <div class="evidence-grid">
                    <div class="evidence-item ${liClass}">
                        <i class="fa-brands fa-linkedin evidence-icon"></i>
                        <div>
                            <span class="evidence-label">LinkedIn Presence</span>
                            <span class="evidence-status">${escapeHtml(liStatus)}</span>
                        </div>
                    </div>
                    <div class="evidence-item ${rdClass}">
                        <i class="fa-brands fa-reddit evidence-icon"></i>
                        <div>
                            <span class="evidence-label">Online Discussions</span>
                            <span class="evidence-status">${escapeHtml(rdStatus)}${rdCountText}</span>
                        </div>
                    </div>
                    <div class="evidence-item ${rvClass}">
                        <i class="fa-solid fa-star evidence-icon"></i>
                        <div>
                            <span class="evidence-label">Employee Reviews</span>
                            <span class="evidence-status">${escapeHtml(rvStatus)}${rvCountText}</span>
                        </div>
                    </div>
                    <div class="evidence-item ${scamClass}">
                        <i class="fa-solid fa-triangle-exclamation evidence-icon"></i>
                        <div>
                            <span class="evidence-label">Scam Complaints</span>
                            <span class="evidence-status">${escapeHtml(scamText)}</span>
                        </div>
                    </div>
                </div>
                ${aiSummaryHtml}
                ${searchUrlsHtml}
            `;
        } else {
            evidenceContent = `
                <div class="social-result-box">
                    <i class="fa-solid fa-building-user social-icon"></i>
                    <span class="social-text">${escapeHtml(socialAnalysis.interpretation || 'No social media footprint available.')}</span>
                </div>
            `;
        }

        socialHtml = `
            <div class="intel-card">
                <div class="intel-header">
                    <div class="intel-header-left">
                        <i class="fa-solid fa-users-viewfinder intel-icon"></i>
                        <div>
                            <span class="intel-title">Online Reputation &amp; Signal Intelligence</span>
                            <span class="intel-sub">Cross-referenced against verified public data</span>
                        </div>
                    </div>
                    <div class="social-header-right">
                        <span class="intel-score-tag">${socialScore}/100</span>
                        ${socialVerificationTag}
                    </div>
                </div>
                <div class="intel-body">
                    ${evidenceContent}
                </div>
            </div>
        `;
    }

    container.innerHTML = `
        <section class="results-wrapper" id="resultsSection">
            <!-- Main Verdict Card -->
            <div class="verdict-card ${cardClass}" id="verdictCard">
                <div class="verdict-header">
                    <div class="verdict-badge">
                        ${badgeHtml}
                    </div>
                    <div class="verdict-actions">
                        <button class="action-btn" id="copyBtn" onclick="copyReportSummary()">
                            <i class="fa-solid fa-copy"></i> <span class="btn-label">Copy Report</span>
                        </button>
                    </div>
                </div>

                <div class="verdict-body">
                    <!-- Left: Circular Radial Score -->
                    <div class="gauge-container">
                        <svg class="radial-gauge" viewBox="0 0 120 120">
                            <circle class="gauge-bg" cx="60" cy="60" r="52"></circle>
                            <circle class="gauge-fill" cx="60" cy="60" r="52" 
                                style="stroke-dashoffset: ${strokeDashoffset};">
                            </circle>
                        </svg>
                        <div class="gauge-center">
                            <span class="score-num">${finalScore}</span>
                            <span class="score-denom">/ 100</span>
                            <span class="score-label">Safety Score</span>
                        </div>
                    </div>

                    <!-- Right: Overall Verdict Details -->
                    <div class="verdict-info">
                        <h3 class="verdict-headline">${headline}</h3>
                        <p class="verdict-desc">
                            Your safety score is calculated by cross-checking historical job data, salary realism, company authenticity, and online reputation.
                        </p>

                        <!-- Score Weighting Transparency -->
                        <div class="score-weights">
                            <span class="weight-item">Pattern Check 30%</span>
                            <span class="weight-sep">+</span>
                            <span class="weight-item">AI Content Check 30%</span>
                            <span class="weight-sep">+</span>
                            <span class="weight-item">Website 20%</span>
                            <span class="weight-sep">+</span>
                            <span class="weight-item">Reputation 20%</span>
                        </div>

                        <div class="risk-pill-row">
                            <span class="risk-meta-item">
                                <strong>Verdict:</strong> ${escapeHtml(prediction)}
                            </span>
                            <span class="risk-meta-item">
                                <strong>Risk Level:</strong> ${escapeHtml(riskLevel)}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 4 Pillars Detection Score Grid -->
            <div class="pillars-section">
                <h3 class="section-title">
                    <i class="fa-solid fa-chart-simple"></i> Safety Breakdown by Category
                </h3>

                <div class="pillars-grid">
                    <!-- Pillar 1: ML Score -->
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <div class="pillar-title">
                                <i class="fa-solid fa-microchip pillar-icon"></i>
                                <span>Pattern Match</span>
                            </div>
                            <span class="pillar-tooltip" title="Matches wording against 17,800+ real and scam job records.">
                                <i class="fa-solid fa-circle-info"></i>
                            </span>
                        </div>
                        <div class="pillar-score">${mlScore}/100</div>
                        <div class="progress-bar-track">
                            <div class="progress-bar-fill" style="width: ${mlScore}%;"></div>
                        </div>
                        <span class="pillar-footer-text">Historical Dataset Match</span>
                    </div>

                    <!-- Pillar 2: AI Score -->
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <div class="pillar-title">
                                <i class="fa-solid fa-wand-magic-sparkles pillar-icon"></i>
                                <span>AI Content Check</span>
                            </div>
                            <span class="pillar-tooltip" title="Checks for unrealistic pay, urgency tricks, fee requests, and odd grammar.">
                                <i class="fa-solid fa-circle-info"></i>
                            </span>
                        </div>
                        <div class="pillar-score">
                            ${aiScore}/100
                            ${aiScoreTag}
                        </div>
                        <div class="progress-bar-track">
                            <div class="progress-bar-fill ${aiBarClass}" style="width: ${aiScore}%;"></div>
                        </div>
                        <span class="pillar-footer-text">${aiFooterText}</span>
                    </div>

                    <!-- Pillar 3: Website Score -->
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <div class="pillar-title">
                                <i class="fa-solid fa-globe pillar-icon"></i>
                                <span>Website Check</span>
                            </div>
                            <span class="pillar-tooltip" title="Scans company website for business information and active operations.">
                                <i class="fa-solid fa-circle-info"></i>
                            </span>
                        </div>
                        <div class="pillar-score">${websiteScore}/100</div>
                        <div class="progress-bar-track">
                            <div class="progress-bar-fill" style="width: ${websiteScore}%;"></div>
                        </div>
                        <span class="pillar-footer-text">Employer Web Presence</span>
                    </div>

                    <!-- Pillar 4: Social Score -->
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <div class="pillar-title">
                                <i class="fa-solid fa-users-viewfinder pillar-icon"></i>
                                <span>Reputation</span>
                            </div>
                            <span class="pillar-tooltip" title="Checks public presence on LinkedIn, employee reviews, and scam warning lists.">
                                <i class="fa-solid fa-circle-info"></i>
                            </span>
                        </div>
                        <div class="pillar-score">${socialScore}/100</div>
                        <div class="progress-bar-track">
                            <div class="progress-bar-fill" style="width: ${socialScore}%;"></div>
                        </div>
                        <span class="pillar-footer-text">${socialFooterText}</span>
                    </div>
                </div>
            </div>

            <!-- Detailed Explanation & Risk Factors -->
            <div class="intel-section">
                <h3 class="section-title">
                    <i class="fa-solid fa-magnifying-glass"></i> Deep Security Audit
                </h3>

                <div class="intel-grid">
                    <!-- AI Risk Analysis Card -->
                    <div class="intel-card">
                        <div class="intel-header">
                            <div class="intel-header-left">
                                <i class="fa-solid fa-brain intel-icon"></i>
                                <div>
                                    <span class="intel-title">AI Tone &amp; Offer Assessment</span>
                                    <span class="risk-badge risk-${riskLevel.toLowerCase()}">${escapeHtml(riskLevel)} Risk</span>
                                </div>
                            </div>
                            <div class="intel-header-right">
                                ${data.ai_unavailable ? '<span class="intel-sub"><i class="fa-solid fa-circle-exclamation"></i> Heuristic Check (AI Busy)</span>' : '<span class="verified-tag"><i class="fa-solid fa-circle-check"></i> Gemini Pro</span>'}
                            </div>
                        </div>
                        <div class="intel-body">
                            <div class="reasons-list">
                                ${reasonsHtml}
                            </div>
                        </div>
                    </div>

                    ${websiteHtml}
                    ${socialHtml}
                </div>
            </div>
        </section>
    `;

    setTimeout(() => {
        const el = document.getElementById('resultsSection');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

        // ================================================================
        // Page Navigation Switcher (Multi-Page SPA Router)
        // ================================================================
        function switchPage(pageId) {
            const pages = document.querySelectorAll('.page-view');
            pages.forEach(p => p.classList.remove('active'));

            const navLinks = document.querySelectorAll('.nav-link');
            navLinks.forEach(l => l.classList.remove('active'));

            const targetPage = document.getElementById(`page-${pageId}`);
            const targetNav  = document.getElementById(`nav-${pageId}`);

            if (targetPage) {
                targetPage.classList.add('active');
            } else {
                document.getElementById('page-analyzer').classList.add('active');
            }

            if (targetNav) targetNav.classList.add('active');

            history.pushState(null, null, `#${pageId}`);

            const menu = document.getElementById('navMenu');
            if (menu) menu.classList.remove('mobile-open');

            window.scrollTo({ top: 0, behavior: 'smooth' });

            if (pageId === 'history') {
                loadHistoryUI();
            } else if (pageId === 'metrics') {
                loadModelMetrics();
            }
        }

        window.addEventListener('hashchange', () => {
            const hash = window.location.hash.replace('#', '') || 'analyzer';
            switchPage(hash);
        });

        function toggleMobileMenu() {
            const menu = document.getElementById('navMenu');
            if (menu) menu.classList.toggle('mobile-open');
        }

        // ================================================================
        // Character & Word Counter
        // ================================================================
        const textarea    = document.getElementById('job_description');
        const charCounter = document.getElementById('charCounter');

        function updateCounts() {
            if (!textarea || !charCounter) return;
            const text      = textarea.value.trim();
            const charCount = text.length;
            const wordCount = text ? text.split(/\s+/).length : 0;
            charCounter.textContent = `${charCount} characters • ${wordCount} words`;
        }

        if (textarea) {
            textarea.addEventListener('input', updateCounts);
            updateCounts();
        }

        // ================================================================
        // Fill Sample Job Descriptions
        // ================================================================
        function fillSample(type) {
            switchPage('analyzer');
            const jobDescInput = document.getElementById('job_description');
            const websiteInput = document.getElementById('company_website');

            if (type === 'real') {
                const sampleText = document.getElementById('realSampleText').innerText;
                jobDescInput.value = sampleText;
                if (websiteInput) websiteInput.value = 'https://www.goldmansachs.com';
            } else if (type === 'fake') {
                const sampleText = document.getElementById('fakeSampleText').innerText;
                jobDescInput.value = sampleText;
                if (websiteInput) websiteInput.value = '';
            }

            updateCounts();
            document.getElementById('analyzerForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // ================================================================
        // Form Submit Loading Overlay & Stage Progression
        // ================================================================
        const form           = document.getElementById('analyzerForm');
        const loadingOverlay = document.getElementById('loadingOverlay');
        const submitBtn       = document.getElementById('submitBtn');

        if (form) {
            form.addEventListener('submit', async function (e) {
                e.preventDefault();
                const jobDesc = textarea.value.trim();
                const website = (document.getElementById('company_website') ? document.getElementById('company_website').value.trim() : '');

                if (!jobDesc) {
                    alert('Please paste a job description first.');
                    return;
                }

                loadingOverlay.classList.add('active');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.querySelector('.btn-text').textContent = 'Scanning Job Safety...';
                }

                const s2 = setTimeout(() => setStageActive('stage2'), 1200);
                const s3 = setTimeout(() => setStageActive('stage3'), 2800);
                const s4 = setTimeout(() => setStageActive('stage4'), 4500);

                try {
                    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            job_description: jobDesc,
                            company_website: website
                        })
                    });

                    clearTimeout(s2);
                    clearTimeout(s3);
                    clearTimeout(s4);

                    const data = await response.json();

                    if (!response.ok || !data.success) {
                        alert(data.error || 'Analysis failed. Please check the job description and try again.');
                        return;
                    }

                    renderResults(data);

                    saveToHistory({
                        verdict:        data.prediction,
                        score:          data.final_score,
                        riskLevel:      data.risk_level || 'N/A',
                        mlResult:       data.prediction,
                        mlScore:        data.ml_score,
                        jobDescription: jobDesc,
                        website:        website,
                        date:           new Date().toISOString()
                    });

                } catch (err) {
                    clearTimeout(s2);
                    clearTimeout(s3);
                    clearTimeout(s4);
                    console.error('Analysis request error:', err);
                    alert('Could not connect to the analysis engine. If the backend is waking up from sleep, please wait 30 seconds and try again.');
                } finally {
                    loadingOverlay.classList.remove('active');
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.querySelector('.btn-text').textContent = 'Run Multi-Layer Scan';
                    }
                    ['stage1', 'stage2', 'stage3', 'stage4'].forEach((id, idx) => {
                        const el = document.getElementById(id);
                        if (el) {
                            el.className = 'stage-item' + (idx === 0 ? ' active' : '');
                            const icon = el.querySelector('.stage-icon');
                            if (icon) icon.className = (idx === 0 ? 'fa-solid fa-spinner fa-spin stage-icon' : 'fa-solid fa-circle stage-icon');
                        }
                    });
                }
            });
        }

        function setStageActive(stageId) {
            const current = document.getElementById(stageId);
            if (!current) return;

            let prev = current.previousElementSibling;
            while (prev) {
                prev.className = 'stage-item done';
                const icon = prev.querySelector('.stage-icon');
                if (icon) icon.className = 'fa-solid fa-circle-check stage-icon';
                prev = prev.previousElementSibling;
            }

            current.className = 'stage-item active';
            const icon = current.querySelector('.stage-icon');
            if (icon) icon.className = 'fa-solid fa-spinner fa-spin stage-icon';
        }

        // ================================================================
        // Copy Audit Summary
        // ================================================================
        function copyReportSummary() {
            const prediction = (currentAnalysisData && currentAnalysisData.prediction) || '';
            const score      = (currentAnalysisData && currentAnalysisData.final_score !== undefined) ? currentAnalysisData.final_score : '';
            const risk       = (currentAnalysisData && currentAnalysisData.risk_level) || '';
            const mlScore    = (currentAnalysisData && currentAnalysisData.ml_score !== undefined) ? currentAnalysisData.ml_score : '';

            const summaryText = [
                `[ShieldJob AI — Job Safety Report]`,
                `Verdict: ${prediction}`,
                `Safety Score: ${score}/100`,
                `Risk Level: ${risk}`,
                `Pattern Match Score: ${mlScore}/100`,
                `Checked with ShieldJob AI.`
            ].join('\n');

            navigator.clipboard.writeText(summaryText).then(() => {
                const btn = document.getElementById('copyBtn');
                if (btn) {
                    btn.innerHTML = '<i class="fa-solid fa-check"></i> <span class="btn-label">Copied!</span>';
                    setTimeout(() => {
                        btn.innerHTML = '<i class="fa-solid fa-copy"></i> <span class="btn-label">Copy Report</span>';
                    }, 2000);
                }
            }).catch(err => {
                console.error('Failed to copy summary:', err);
            });
        }

        // ================================================================
        // Analysis History (localStorage) with Full Job Description
        // ================================================================
        const HISTORY_KEY = 'shieldjob_history';
        const HISTORY_MAX = 15;
        let currentModalJobIndex = -1;

        function saveToHistory(entry) {
            let history = getHistory();
            const now = Date.now();
            const recent = history.find(h => {
                const diff = Math.abs(new Date(h.date).getTime() - now);
                return h.verdict === entry.verdict && h.score === entry.score && diff < 60000;
            });
            if (recent) return;

            history.unshift(entry);
            history = history.slice(0, HISTORY_MAX);
            try {
                localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
            } catch(e) {
                console.warn('localStorage unavailable:', e);
            }
            updateNavBadge();
        }

        function getHistory() {
            try {
                const raw = localStorage.getItem(HISTORY_KEY);
                if (!raw) return [];
                const parsed = JSON.parse(raw);
                if (!Array.isArray(parsed)) return [];
                return parsed;
            } catch(e) {
                return [];
            }
        }

        function deleteHistoryItem(index) {
            let history = getHistory();
            history.splice(index, 1);
            try {
                localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
            } catch(e) {}
            loadHistoryUI();
            updateNavBadge();
        }

        function clearAllHistory() {
            try {
                localStorage.removeItem(HISTORY_KEY);
            } catch(e) {}
            loadHistoryUI();
            updateNavBadge();
        }

        function updateNavBadge() {
            const history = getHistory();
            const badge = document.getElementById('historyNavBadge');
            if (badge) {
                badge.textContent = history.length;
                badge.style.display = history.length > 0 ? 'inline-flex' : 'none';
            }
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function loadHistoryUI() {
            const history = getHistory();
            const emptyEl      = document.getElementById('historyEmpty');
            const tableWrapper = document.getElementById('historyTableWrapper');
            const tbody        = document.getElementById('historyTableBody');

            const total = history.length;
            const reals = history.filter(h => h.verdict === 'Real Job').length;
            const fakes = history.filter(h => h.verdict !== 'Real Job').length;

            const statTotal = document.getElementById('statTotalCount');
            const statReal  = document.getElementById('statRealCount');
            const statFake  = document.getElementById('statFakeCount');

            if (statTotal) statTotal.textContent = total;
            if (statReal)  statReal.textContent  = reals;
            if (statFake)  statFake.textContent  = fakes;

            if (!history.length) {
                if (emptyEl) emptyEl.style.display = 'flex';
                if (tableWrapper) tableWrapper.style.display = 'none';
                return;
            }

            if (emptyEl) emptyEl.style.display = 'none';
            if (tableWrapper) tableWrapper.style.display = 'block';

            if (tbody) {
                tbody.innerHTML = '';
                history.forEach((item, i) => {
                    const date = new Date(item.date);
                    const dateStr = date.toLocaleDateString('en-IN', {
                        day: '2-digit', month: 'short', year: 'numeric',
                        hour: '2-digit', minute: '2-digit'
                    });

                    const verdictClass = item.verdict === 'Real Job' ? 'verdict-tag-real'
                        : item.verdict === 'Suspicious Job' ? 'verdict-tag-suspicious'
                        : 'verdict-tag-fake';

                    const riskClass = (item.riskLevel || '').toLowerCase() === 'low' ? 'risk-low'
                        : (item.riskLevel || '').toLowerCase() === 'high' ? 'risk-high'
                        : 'risk-medium';

                    // Extract a clean title or snippet
                    let jobSnippet = 'Job Posting #' + (i + 1);
                    if (item.jobDescription) {
                        const firstLine = item.jobDescription.trim().split('\n')[0].trim();
                        jobSnippet = firstLine.length > 55 ? firstLine.substring(0, 55) + '...' : firstLine;
                    }

                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>
                            <div class="history-job-clickable" onclick="openJobModal(${i})" title="Click to view full job description">
                                <i class="fa-solid fa-file-lines job-icon"></i>
                                <span class="job-title-text">${escapeHtml(jobSnippet)}</span>
                                <i class="fa-solid fa-up-right-from-square expand-icon"></i>
                            </div>
                        </td>
                        <td><span class="verdict-tag ${verdictClass}">${item.verdict}</span></td>
                        <td><strong>${item.score}</strong>/100</td>
                        <td><span class="risk-badge ${riskClass}">${item.riskLevel || 'N/A'}</span></td>
                        <td class="history-date">${dateStr}</td>
                        <td>
                            <button class="history-delete-btn" onclick="deleteHistoryItem(${i})" title="Delete this entry">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        // ================================================================
        // Job Description Full View Modal
        // ================================================================
        function openJobModal(index) {
            const history = getHistory();
            const item = history[index];
            if (!item) return;

            currentModalJobIndex = index;
            const modal = document.getElementById('jobModalOverlay');
            const content = document.getElementById('jobModalContent');
            const meta = document.getElementById('jobModalMeta');

            const date = new Date(item.date).toLocaleString();
            const verdictClass = item.verdict === 'Real Job' ? 'verdict-tag-real'
                : item.verdict === 'Suspicious Job' ? 'verdict-tag-suspicious'
                : 'verdict-tag-fake';

            meta.innerHTML = `
                <span class="verdict-tag ${verdictClass}">${item.verdict}</span>
                <span class="risk-meta-item"><strong>Score:</strong> ${item.score}/100</span>
                <span class="risk-meta-item"><strong>Risk:</strong> ${item.riskLevel || 'N/A'}</span>
                <span class="history-date"><i class="fa-regular fa-clock"></i> ${date}</span>
            `;

            content.textContent = item.jobDescription || "No full job description saved for this entry.";
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeJobModal() {
            const modal = document.getElementById('jobModalOverlay');
            if (modal) modal.classList.remove('active');
            document.body.style.overflow = '';
            currentModalJobIndex = -1;
        }

        function copyModalJobText() {
            const history = getHistory();
            const item = history[currentModalJobIndex];
            if (!item || !item.jobDescription) return;

            navigator.clipboard.writeText(item.jobDescription).then(() => {
                const btn = document.getElementById('modalCopyBtn');
                if (btn) {
                    btn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
                    setTimeout(() => {
                        btn.innerHTML = '<i class="fa-solid fa-copy"></i> Copy Text';
                    }, 2000);
                }
            });
        }

        function reanalyzeModalJob() {
            const history = getHistory();
            const item = history[currentModalJobIndex];
            if (!item || !item.jobDescription) return;

            closeJobModal();
            switchPage('analyzer');

            const jobDescInput = document.getElementById('job_description');
            const websiteInput = document.getElementById('company_website');

            if (jobDescInput) jobDescInput.value = item.jobDescription;
            if (websiteInput) websiteInput.value = item.website || '';

            updateCounts();
            document.getElementById('analyzerForm').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // Close modal with Escape key
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeJobModal();
        });

        // ================================================================
        // Load Model Metrics from /api/model-metrics
        // ================================================================
        function loadModelMetrics() {
            const grid = document.getElementById('metricsGrid');
            if (!grid) return;

            fetch(`${API_BASE_URL}/api/model-metrics`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'not_computed') {
                        grid.innerHTML = `
                            <div class="metrics-not-computed">
                                <i class="fa-solid fa-circle-info"></i>
                                <p>${data.message}</p>
                            </div>`;
                        return;
                    }
                    if (data.status !== 'ok') {
                        grid.innerHTML = `<div class="metrics-not-computed"><i class="fa-solid fa-circle-info"></i><p>Metrics unavailable.</p></div>`;
                        return;
                    }

                    const m  = data.metrics.metrics;
                    const ds = data.metrics.dataset_info;
                    const mi = data.metrics.model_info;
                    const cm = data.metrics.confusion_matrix;

                    const sampleTag = document.getElementById('cmSampleTag');
                    if (sampleTag) {
                        sampleTag.textContent = `${ds.total_samples.toLocaleString()} Postings Evaluated (${mi.evaluation_method || '5-Fold CV'})`;
                    }

                    const metricCards = [
                        {
                            key:   'Overall Accuracy',
                            value: m.accuracy,
                            icon:  'fa-bullseye',
                            desc:  `Tested accuracy across all ${ds.total_samples.toLocaleString()} postings (Baseline: ${ds.baseline_accuracy_pct || '95.16'}%).`
                        },
                        {
                            key:   'Scam Catch Rate (Recall)',
                            value: m.recall,
                            icon:  'fa-radar',
                            desc:  `Catches ${m.recall}% of all fraudulent job postings and scam variations.`
                        },
                        {
                            key:   'Precision (Reliability)',
                            value: m.precision,
                            icon:  'fa-crosshairs',
                            desc:  `When flagged as a scam, it is accurate ${m.precision}% of the time with minimal false alarms.`
                        },
                        {
                            key:   'Balanced Reliability (F1)',
                            value: m.f1_score,
                            icon:  'fa-scale-balanced',
                            desc:  'Harmonic balance between precision and scam detection rate.'
                        },
                        {
                            key:   'Distinction Power (ROC-AUC)',
                            value: m.roc_auc,
                            icon:  'fa-chart-area',
                            desc:  'Strong capability to separate genuine offers from scams across thresholds.'
                        },
                    ];

                    grid.innerHTML = `
                        <div class="metrics-info-bar">
                            <span><i class="fa-solid fa-robot"></i> Classifier: <strong>${mi.name}</strong></span>
                            <span><i class="fa-solid fa-database"></i> Dataset: <strong>${ds.total_samples.toLocaleString()}</strong> postings</span>
                            <span><i class="fa-solid fa-vial"></i> Validation: <strong>${mi.evaluation_method || '5-Fold Stratified CV'}</strong></span>
                            <span><i class="fa-solid fa-percent"></i> Dataset Fraud Rate: <strong>${ds.fraud_rate_pct}%</strong></span>
                        </div>
                        ${metricCards.map(mc => `
                        <div class="metric-card">
                            <div class="metric-header">
                                <i class="fa-solid ${mc.icon} metric-icon"></i>
                                <span class="metric-name">${mc.key}</span>
                            </div>
                            <div class="metric-value">${mc.value}%</div>
                            <div class="metric-bar-track">
                                <div class="metric-bar-fill" style="width:${mc.value}%"></div>
                            </div>
                            <p class="metric-desc">${mc.desc}</p>
                        </div>`).join('')}
                    `;

                    const confusionSection = document.getElementById('confusionSection');
                    const confusionMatrix  = document.getElementById('confusionMatrix');
                    const cmLegend         = document.getElementById('cmLegend');

                    if (confusionSection) confusionSection.style.display = 'block';
                    if (confusionMatrix) {
                        confusionMatrix.innerHTML = `
                            <thead>
                                <tr>
                                    <th></th>
                                    <th>Identified as Real</th>
                                    <th>Identified as Scam</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th>Actual Real Jobs</th>
                                    <td class="cm-tn-cell">${cm.true_negatives.toLocaleString()}<br><small>Genuine Job Approved</small></td>
                                    <td class="cm-fp-cell">${cm.false_positives.toLocaleString()}<br><small>False Alarm</small></td>
                                </tr>
                                <tr>
                                    <th>Actual Scam Jobs</th>
                                    <td class="cm-fn-cell">${cm.false_negatives.toLocaleString()}<br><small>Edge-case Scam</small></td>
                                    <td class="cm-tp-cell">${cm.true_positives.toLocaleString()}<br><small>Scam Successfully Caught</small></td>
                                </tr>
                            </tbody>
                        `;
                    }

                    if (cmLegend) {
                        cmLegend.innerHTML = `
                            <div class="cm-legend-item">
                                <span class="cm-dot cm-tp"></span>
                                <div><strong>Scams Caught (${cm.true_positives.toLocaleString()}):</strong> Fraudulent job postings successfully flagged.</div>
                            </div>
                            <div class="cm-legend-item">
                                <span class="cm-dot cm-tn"></span>
                                <div><strong>Real Jobs Approved (${cm.true_negatives.toLocaleString()}):</strong> Genuine employment opportunities approved.</div>
                            </div>
                            <div class="cm-legend-item">
                                <span class="cm-dot cm-fp"></span>
                                <div><strong>False Alarms (${cm.false_positives.toLocaleString()}):</strong> Real jobs conservatively flagged (${((cm.false_positives / ds.legitimate_jobs) * 100).toFixed(1)}% of genuine jobs).</div>
                            </div>
                            <div class="cm-legend-item">
                                <span class="cm-dot cm-fn"></span>
                                <div><strong>Edge Cases Missed (${cm.false_negatives.toLocaleString()}):</strong> Handled by ShieldJob AI's secondary Gemini AI and reputation layers.</div>
                            </div>
                        `;
                    }
                })
                .catch(err => {
                    if (grid) grid.innerHTML = `<div class="metrics-not-computed"><i class="fa-solid fa-circle-info"></i><p>Could not load accuracy data.</p></div>`;
                });
        }

        // ================================================================
        // Initial Startup
        // ================================================================
        window.addEventListener('DOMContentLoaded', () => {
            const initialHash = window.location.hash.replace('#', '') || 'analyzer';
            switchPage(initialHash);

            // Analysis completed via client-side fetch

            updateNavBadge();
            loadModelMetrics();
        });
    </script>
