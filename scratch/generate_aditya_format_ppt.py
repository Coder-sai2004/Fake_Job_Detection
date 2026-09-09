import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def generate_aditya_format_ppt():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    logo_path = r"c:\Users\Ram Sai\OneDrive\Desktop\PROJECTS\Fake_Job_Detection\scratch\template_assets\img_1_0_Picture 1.jpg"

    # Template Color Palette (Times New Roman / Aditya University Standard)
    COLOR_PRIMARY_NAVY = RGBColor(0, 32, 96)      # #002060 Deep Academic Navy
    COLOR_BODY_TEXT = RGBColor(20, 20, 20)        # #141414 Off Black
    COLOR_MUTED_FOOTER = RGBColor(127, 127, 127)  # #7F7F7F Gray
    COLOR_SUBTITLE = RGBColor(31, 78, 121)        # #1F4E79 Dark Slate Blue
    PROJECT_NAME_FOOTER = "ShieldJob AI: Multi-Modal Fake Job Detection System"

    def add_slide_header_and_footer(slide, title_text, slide_number):
        # 1. College Logo (Top Left)
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(0.36), Inches(0.34), width=Inches(3.08), height=Inches(0.71))

        # 2. Slide Title Header (Top Right / Center)
        tx_title = slide.shapes.add_textbox(Inches(3.30), Inches(0.28), Inches(9.50), Inches(0.95))
        tf = tx_title.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text.upper()
        p.font.name = "Times New Roman"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY_NAVY

        # 3. Footer Left (Project Title)
        tx_foot_l = slide.shapes.add_textbox(Inches(0.36), Inches(6.85), Inches(8.50), Inches(0.40))
        tf_l = tx_foot_l.text_frame
        tf_l.word_wrap = True
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = PROJECT_NAME_FOOTER
        p_l.font.name = "Times New Roman"
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = COLOR_MUTED_FOOTER

        # 4. Footer Right (Slide Number)
        tx_foot_r = slide.shapes.add_textbox(Inches(11.80), Inches(6.85), Inches(1.00), Inches(0.40))
        tf_r = tx_foot_r.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = str(slide_number)
        p_r.font.name = "Times New Roman"
        p_r.font.size = Pt(11)
        p_r.font.color.rgb = COLOR_MUTED_FOOTER
        p_r.alignment = PP_ALIGN.RIGHT

    def add_bullet_content(slide, points, top=1.45, height=5.20, font_size=18, space_after=12):
        tx_content = slide.shapes.add_textbox(Inches(0.85), Inches(top), Inches(11.60), Inches(height))
        tf = tx_content.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for i, (label, text) in enumerate(points):
            p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
            p.space_after = Pt(space_after)
            p.line_spacing = 1.25

            # Bullet and bold prefix
            r1 = p.add_run()
            r1.text = f"•  {label}: " if label else "•  "
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(font_size)
            r1.font.bold = True
            r1.font.color.rgb = COLOR_PRIMARY_NAVY

            # Body description
            r2 = p.add_run()
            r2.text = text
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(font_size)
            r2.font.bold = False
            r2.font.color.rgb = COLOR_BODY_TEXT

    # ==================== SLIDE 1: TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(3.56), Inches(0.20), width=Inches(6.22), height=Inches(1.43))

    # Title & Subtitle Box
    tx_s1_title = s1.shapes.add_textbox(Inches(0.80), Inches(1.80), Inches(11.73), Inches(1.50))
    tf_s1_title = tx_s1_title.text_frame
    tf_s1_title.word_wrap = True
    tf_s1_title.margin_left = tf_s1_title.margin_top = tf_s1_title.margin_right = tf_s1_title.margin_bottom = 0

    p_t = tf_s1_title.paragraphs[0]
    p_t.text = "SHIELDJOB AI – MULTI-MODAL FAKE JOB DETECTION SYSTEM"
    p_t.font.name = "Times New Roman"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY_NAVY
    p_t.alignment = PP_ALIGN.CENTER
    p_t.space_after = Pt(6)

    p_sub = tf_s1_title.add_paragraph()
    p_sub.text = "An AI/ML-Powered Verification Platform for Automated Recruitment Scam Detection & Trust Scoring"
    p_sub.font.name = "Times New Roman"
    p_sub.font.size = Pt(16)
    p_sub.font.italic = True
    p_sub.font.color.rgb = COLOR_SUBTITLE
    p_sub.alignment = PP_ALIGN.CENTER

    # Presenter Information Box
    tx_s1_pres = s1.shapes.add_textbox(Inches(1.50), Inches(3.50), Inches(10.33), Inches(3.50))
    tf_s1_pres = tx_s1_pres.text_frame
    tf_s1_pres.word_wrap = True
    tf_s1_pres.margin_left = tf_s1_pres.margin_top = tf_s1_pres.margin_right = tf_s1_pres.margin_bottom = 0

    pres_lines = [
        ("Presented By", True, Pt(17), COLOR_PRIMARY_NAVY, Pt(4)),
        ("Tanuku Ram Sai  (PIN: 24A95A0503)", True, Pt(19), COLOR_BODY_TEXT, Pt(8)),
        ("Department of Computer Science & Engineering", False, Pt(16), COLOR_BODY_TEXT, Pt(2)),
        ("Aditya University, Surampalem", False, Pt(16), COLOR_BODY_TEXT, Pt(14)),
        ("Internship Organization: VedXlence Innovations Pvt. Ltd., Hyderabad", True, Pt(15), COLOR_PRIMARY_NAVY, Pt(2)),
        ("Program: AICTE Certified Internship & Upskilling Program | Domain: Machine Learning with Python", False, Pt(14), COLOR_BODY_TEXT, Pt(2)),
        ("Internship Duration: May 6, 2026 – July 5, 2026 (Offline Mode)", False, Pt(14), COLOR_BODY_TEXT, Pt(0))
    ]

    for i, (l_text, l_bold, l_size, l_color, l_space) in enumerate(pres_lines):
        p_l = tf_s1_pres.add_paragraph() if i > 0 else tf_s1_pres.paragraphs[0]
        p_l.text = l_text
        p_l.font.name = "Times New Roman"
        p_l.font.size = l_size
        p_l.font.bold = l_bold
        p_l.font.color.rgb = l_color
        p_l.alignment = PP_ALIGN.CENTER
        p_l.space_after = l_space

    # ==================== SLIDE 2: INTERNSHIP OVERVIEW ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s2, "INTERNSHIP OVERVIEW", 2)
    add_bullet_content(s2, [
        ("Host Organization", "VedXlence Innovations Pvt. Ltd., Hyderabad, Telangana, India."),
        ("Internship Domain", "Machine Learning with Python and Natural Language Processing."),
        ("Program Nature", "AICTE Certified Internship & Upskilling Program."),
        ("Duration & Timeline", "2 Months intensive program, from May 6, 2026 to July 5, 2026."),
        ("Internship Mode", "Offline training and project implementation mode."),
        ("Official Portal", "https://www.vedxlence.in/")
    ], font_size=18, space_after=14)

    # ==================== SLIDE 3: ORGANIZATION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s3, "ORGANIZATION PROFILE", 3)
    add_bullet_content(s3, [
        ("Organization Background", "VedXlence Innovations Pvt. Ltd. is an emerging technology enterprise headquartered in Hyderabad, Telangana."),
        ("AICTE-Certified Program", "Conducted an AICTE-certified internship and upskilling program tailored to build high-demand industry skills."),
        ("Technical Training", "Provided structured training covering core Python, machine learning workflows, NLP text analysis, and API design."),
        ("Real-World Project Execution", "Emphasized end-to-end practical project development, bridging academic knowledge with production requirements."),
        ("Professional Growth", "Instilled best practices in software development, collaborative version control, testing, and cloud deployment.")
    ], font_size=18, space_after=14)

    # ==================== SLIDE 4: WORK & RESPONSIBILITIES ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s4, "INTERNSHIP WORK & RESPONSIBILITIES", 4)
    add_bullet_content(s4, [
        ("Data Preprocessing & EDA", "Cleaned, structured, and analyzed 17,880 job records from the benchmark EMSCAD dataset."),
        ("NLP & Feature Extraction", "Applied TF-IDF vectorization to convert raw job texts and requirements into numerical feature matrices."),
        ("ML Model Development", "Trained and tuned a Balanced Random Forest Classifier to handle severe real-world class imbalance."),
        ("Generative AI Integration", "Integrated Google Gemini 2.5 Flash API with specialized prompt engineering for semantic red-flag detection."),
        ("Multi-Modal Verification", "Implemented automated company website health checks and public social-footprint verification using BeautifulSoup."),
        ("Application & Deployment", "Engineered a Flask web application, Chrome Extension (Manifest V3), and deployed the live system on Render.")
    ], font_size=17, space_after=11)

    # ==================== SLIDE 5: SKILLS LEARNED ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s5, "SKILLS & TECHNOLOGIES LEARNED", 5)
    add_bullet_content(s5, [
        ("Backend Development", "Python 3, Flask Web Framework, Gunicorn WSGI Server, RESTful API architecture."),
        ("Machine Learning & NLP", "Scikit-learn, Balanced Random Forest, TF-IDF Vectorization, Performance Evaluation Metrics."),
        ("Generative AI & LLMs", "Google Gemini 2.5 Flash API, prompt engineering, structured JSON response extraction."),
        ("Web Scraping & APIs", "BeautifulSoup4, Requests library, automated HTTP response verification, search APIs."),
        ("Frontend & Browser Extension", "HTML5, Vanilla CSS3, JavaScript (ES6+), Chrome Extension Manifest V3."),
        ("DevOps & Version Control", "Git version control, GitHub collaboration, Render cloud deployment.")
    ], font_size=17, space_after=11)

    # ==================== SLIDE 6: PROJECT INTRODUCTION ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s6, "PROJECT INTRODUCTION: SHIELDJOB AI", 6)
    add_bullet_content(s6, [
        ("The Problem", "A massive surge in online recruitment scams, phishing traps, and fraudulent job postings targeting vulnerable job seekers."),
        ("Project Objective", "To automatically evaluate and classify job postings as legitimate, suspicious, or potentially fraudulent with high precision."),
        ("Multi-Modal Approach", "Overcomes the vulnerabilities of text-only filters by combining Machine Learning, Generative AI, website status, and public footprint analysis."),
        ("Trust Rating System", "Aggregates multi-source evidence into an explainable 0–100 Safety Score with highlighted red flags."),
        ("Dual Platform Access", "Delivered as an interactive Flask Web Portal and an on-the-go Chrome Extension for real-time protection on job boards.")
    ], font_size=18, space_after=14)

    # ==================== SLIDE 7: PROJECT WORKFLOW ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s7, "PROJECT WORKFLOW & ARCHITECTURE", 7)
    add_bullet_content(s7, [
        ("Step 1 – Input Ingestion", "User submits job details via Web Form or auto-captures text from job boards via Chrome Extension."),
        ("Step 2 – Machine Learning Analysis (30%)", "Balanced Random Forest model evaluates text patterns and structural features for fraud signals."),
        ("Step 3 – Gemini AI Contextual Check (30%)", "LLM analyzes subtle contextual red flags, unrealistic compensations, and suspicious contact methods."),
        ("Step 4 – Company Website Verification (20%)", "Automated validation of official corporate domain status, HTTPS availability, and site responsiveness."),
        ("Step 5 – Social & Public Footprint (20%)", "Verifies corporate identity, digital footprint, and search credibility across public web directories."),
        ("Step 6 – Safety Score & Verdict", "Calculates composite 0–100 Safety Score and outputs verdict with human-readable explanation.")
    ], font_size=17, space_after=11)

    # ==================== SLIDE 8: PROJECT FEATURES ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s8, "KEY PROJECT FEATURES", 8)
    add_bullet_content(s8, [
        ("Multi-Layer Scam Detection", "Provides robust defense against sophisticated phishing, fake offers, and financial recruitment frauds."),
        ("AI-Powered Semantic Analysis", "Detects subtle linguistic inconsistencies, suspicious urgency, and unauthorized communication channels."),
        ("Automated Domain & Digital Validation", "Performs real-time domain health checks and public company footprint verification."),
        ("Unified 0–100 Safety Score", "Presents an intuitive, color-coded confidence score for rapid user decision-making."),
        ("Explainable Red-Flag Alerts", "Itemizes exact reasons behind a low score, empowering users with actionable safety insights."),
        ("Dual-Interface Flexibility", "Full-featured Flask web portal complemented by an instant-scan Chrome Extension.")
    ], font_size=18, space_after=13)

    # ==================== SLIDE 9: RESULTS & OUTCOMES ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s9, "RESULTS & PERFORMANCE METRICS", 9)
    add_bullet_content(s9, [
        ("Dataset Benchmark", "Trained on the EMSCAD benchmark dataset containing 17,880 real-world job posting records."),
        ("Core ML Classifier", "Balanced Random Forest Classifier addressing severe class imbalance in recruitment data."),
        ("Primary Accuracy Result", "Achieved an outstanding 98.05% overall classification accuracy."),
        ("Precision & Recall", "79.10% Precision (low false alarms) and 81.29% Recall (high fraud capture rate)."),
        ("F1-Score & ROC-AUC", "F1-Score of 80.18% and ROC-AUC of 98.49%, demonstrating superior class discrimination."),
        ("Production Deployment", "Successfully deployed and operational on Render cloud platform with public GitHub repository.")
    ], font_size=18, space_after=13)

    # ==================== SLIDE 10: KEY LEARNINGS ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s10, "KEY LEARNINGS & TAKEAWAYS", 10)
    add_bullet_content(s10, [
        ("Applied Machine Learning", "Gained deep practical experience in data preprocessing, TF-IDF feature extraction, and ensemble tuning."),
        ("Generative AI Integration", "Mastered LLM API integration (Gemini 2.5 Flash), prompt engineering, and combining ML with GenAI."),
        ("Full-Stack & Extension Engineering", "Engineered REST APIs in Flask, dynamic user interfaces, and Chrome Manifest V3 extensions."),
        ("Web Automation & Scraping", "Built automated web scrapers with BeautifulSoup and implemented real-time HTTP verification."),
        ("Cloud Deployment & Reliability", "Configured production servers with Gunicorn, handled edge cases, and deployed live to Render.")
    ], font_size=18, space_after=14)

    # ==================== SLIDE 11: DEMO TRANSITION ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s11, "PROJECT DEMONSTRATION TRANSITION", 11)
    add_bullet_content(s11, [
        ("Transition to Live Demo", "Concluding the presentation overview to demonstrate the ShieldJob AI system in real time."),
        ("Live Web Application Demonstration", "Testing legitimate and fraudulent job postings on the live Flask web portal."),
        ("Chrome Extension Live Scan", "Demonstrating on-the-fly job verification directly on job portal postings."),
        ("Verification Breakdown", "Observing real-time ML classification, Gemini AI red-flag detection, and 0–100 Safety Score calculation.")
    ], font_size=19, space_after=16)

    # ==================== SLIDE 12: SPEAKING SCRIPT (SLIDES 1 TO 3) ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s12, "SPEAKING SCRIPT: SLIDES 1 TO 3", 12)
    add_bullet_content(s12, [
        ("Slide 1 — Title & Overview (~35s)", "\"Respected panel members and faculty, good morning. Today, I am presenting my internship review on the work I completed at VedXlence Innovations Pvt. Ltd., Hyderabad. I completed a two-month offline internship in Machine Learning with Python from May 6, 2026 to July 5, 2026 under the AICTE-certified upskilling program.\""),
        ("Slide 2 — Internship Overview (~30s)", "\"VedXlence Innovations provided structured technical training and hands-on project implementation, helping bridge academic machine learning concepts with production-ready software development.\""),
        ("Slide 3 — Work & Responsibilities (~45s)", "\"During this internship, my responsibilities spanned the complete development lifecycle: data preprocessing on 17,880 job records, NLP feature extraction with TF-IDF, training a Balanced Random Forest classifier, integrating Gemini AI, building website and social footprint checkers, developing a Flask web app and Chrome extension, and deploying to Render.\"")
    ], font_size=16, space_after=12)

    # ==================== SLIDE 13: SPEAKING SCRIPT (SLIDES 4 TO 7) ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s13, "SPEAKING SCRIPT: SLIDES 4 TO 7", 13)
    add_bullet_content(s13, [
        ("Slide 4 — Skills Learned (~40s)", "\"I developed competencies in Python, Flask, Scikit-learn, and NLP, along with Generative AI prompt engineering with Gemini 2.5 Flash, web scraping with BeautifulSoup, Chrome Extension development, Git version control, and cloud deployment on Render.\""),
        ("Slide 5 — Project Introduction (~45s)", "\"As my capstone project, I built ShieldJob AI – a Multi-Modal Fake Job Detection System. It tackles the growing menace of recruitment scams by automatically evaluating whether a job posting is legitimate, suspicious, or fraudulent using multi-modal cross-verification.\""),
        ("Slide 6 — Workflow & Weights (~45s)", "\"The system integrates four checks: ML text analysis (30%), Gemini AI contextual analysis (30%), company website verification (20%), and public social footprint checking (20%). These compute a unified 0–100 Safety Score with explainable red flags.\""),
        ("Slide 7 — Key Features (~35s)", "\"Features include multi-layer fraud detection, AI content analysis, real-time website validation, a 0–100 trust score, explainable red flags, and dual access via web application and Chrome extension.\"")
    ], font_size=15, space_after=10)

    # ==================== SLIDE 14: SPEAKING SCRIPT (SLIDES 8 TO 11) ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_slide_header_and_footer(s14, "SPEAKING SCRIPT: SLIDES 8 TO 11", 14)
    add_bullet_content(s14, [
        ("Slide 8 — Results & Metrics (~40s)", "\"Trained on 17,880 postings from the EMSCAD dataset, our Balanced Random Forest model achieved 98.05% overall accuracy, 98.49% ROC-AUC, 79.10% precision, and 81.29% recall, fully deployed and operational on Render.\""),
        ("Slide 9 — Key Learnings (~35s)", "\"This internship provided me with practical end-to-end experience in machine learning pipelines, GenAI orchestration, browser extension engineering, and cloud deployment.\""),
        ("Slide 10 & 11 — Demo Transition (~15s)", "\"I have now presented the internship summary and project design. I will now transition to the live demonstration of the ShieldJob AI application and Chrome extension to show the system working in real time. Thank you.\"")
    ], font_size=16, space_after=12)

    # ==================== SLIDE 15: THANK YOU ====================
    s15 = prs.slides.add_slide(blank_layout)
    if os.path.exists(logo_path):
        s15.shapes.add_picture(logo_path, Inches(3.56), Inches(0.40), width=Inches(6.22), height=Inches(1.43))

    tx_ty = s15.shapes.add_textbox(Inches(1.00), Inches(2.20), Inches(11.33), Inches(4.50))
    tf_ty = tx_ty.text_frame
    tf_ty.word_wrap = True
    tf_ty.margin_left = tf_ty.margin_top = tf_ty.margin_right = tf_ty.margin_bottom = 0

    pty1 = tf_ty.paragraphs[0]
    pty1.text = "THANK YOU"
    pty1.font.name = "Times New Roman"
    pty1.font.size = Pt(44)
    pty1.font.bold = True
    pty1.font.color.rgb = COLOR_PRIMARY_NAVY
    pty1.alignment = PP_ALIGN.CENTER
    pty1.space_after = Pt(8)

    pty2 = tf_ty.add_paragraph()
    pty2.text = "Questions & Discussion"
    pty2.font.name = "Times New Roman"
    pty2.font.size = Pt(22)
    pty2.font.bold = True
    pty2.font.color.rgb = COLOR_SUBTITLE
    pty2.alignment = PP_ALIGN.CENTER
    pty2.space_after = Pt(20)

    pty3 = tf_ty.add_paragraph()
    pty3.text = "Tanuku Ram Sai  (PIN: 24A95A0503)\nDepartment of Computer Science & Engineering\nAditya University, Surampalem"
    pty3.font.name = "Times New Roman"
    pty3.font.size = Pt(17)
    pty3.font.bold = False
    pty3.font.color.rgb = COLOR_BODY_TEXT
    pty3.alignment = PP_ALIGN.CENTER

    # Save to target destination and local folder
    target_path = r"C:\Users\Ram Sai\OneDrive\Documents\24A95A0503_T.Ram Sai_internship\Fake_Job_Detection_Internship_Review_Presentation_Aditya_Format.pptx"
    local_path = r"c:\Users\Ram Sai\OneDrive\Desktop\PROJECTS\Fake_Job_Detection\Fake_Job_Detection_Internship_Review_Presentation_Aditya_Format.pptx"

    prs.save(target_path)
    prs.save(local_path)
    print(f"Generated new Aditya-format PPT at:\n1. {target_path}\n2. {local_path}")

if __name__ == "__main__":
    generate_aditya_format_ppt()
