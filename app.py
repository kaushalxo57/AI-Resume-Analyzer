import streamlit as st
import os
import textwrap
from dotenv import load_dotenv

# Import our custom utilities
from utils.parser import extract_text_from_pdf
from utils.scorer import (
    calculate_local_score,
    extract_skills_locally,
    extract_missing_keywords_locally,
    analyze_with_gemini
)
from utils.recommendations import generate_local_suggestions
from utils.resume_summary import generate_local_summary
from utils.role_predictor import predict_roles_locally
from utils.health_analyzer import analyze_resume_health_locally
from utils.report_generator import generate_pdf_report

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="👹",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load and inject custom CSS stylesheet
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

# Main Application Title (Hero)
st.markdown(
    """
    <div class="hero-container">
        <div class="japanese-badge">AI レジュメ 分析</div>
        <h1 class="hero-title">AI RESUME<br>ANALYZER</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Read API Key from session state or environment before rendering the widget
api_key_value = st.session_state.get("gemini_api_key", os.getenv("GEMINI_API_KEY", ""))

# Initialize session state for analysis results
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# SECTION 2: Resume Upload and Inputs
with st.container(border=True):
    st.markdown("### Upload Resume & Job Description")

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF format)",
        type=["pdf"],
        help="Upload your CV or resume in PDF format to parse and analyze.",
        label_visibility="collapsed"
    )

    job_desc = st.text_area(
        "Target Job Description",
        height=150,
        placeholder="Paste target job description to match keywords and skills..."
    )

    analyze_clicked = st.button("RUN ANALYSIS")

# Processing the Analysis
if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a PDF resume before running the analysis.")
    elif not job_desc.strip():
        st.error("Please paste the target job description before running the analysis.")
    else:
        with st.spinner("AUDITING RESUME MATCHING AND ALIGNMENT..."):
            try:
                # 1. Parse PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                analysis = {}
                
                # 2. Check if we should use Gemini or local heuristics
                use_gemini = bool(api_key_value.strip())
                gemini_success = False
                
                if use_gemini:
                    # Attempt Gemini analysis
                    gemini_result = analyze_with_gemini(api_key_value.strip(), resume_text, job_desc)
                    if "error" not in gemini_result:
                        analysis = gemini_result
                        gemini_success = True
                    else:
                        st.warning("Failed to run Gemini analysis (falling back to local NLP engine).")

                if not gemini_success:
                    # Run Local NLP Heuristics
                    scores = calculate_local_score(resume_text, job_desc)
                    skills = extract_skills_locally(resume_text)
                    missing = extract_missing_keywords_locally(resume_text, job_desc)
                    summary = generate_local_summary(resume_text, skills)
                    roles = predict_roles_locally(skills)
                    health = analyze_resume_health_locally(resume_text, skills)
                    suggestions = generate_local_suggestions(scores["score"], missing, skills)
                    
                    analysis = {
                        "score": scores["score"],
                        "classification": scores["classification"],
                        "skills_extracted": skills,
                        "missing_keywords": missing,
                        "professional_summary": summary,
                        "role_predictions": roles,
                        "health_analysis": health,
                        "improvement_suggestions": suggestions
                    }
                
                # Save results to session state
                st.session_state.analysis_results = analysis
                st.success("Analysis complete!")
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

# SECTION 3: Results Dashboard Display
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    # 1. ATS MATCH SCORE CARD (Primary Focus)
    score = results.get("score", 0)
    classification = results.get("classification", "Average")
    class_lower = classification.lower()
    
    st.markdown("---")
    st.markdown(
        textwrap.dedent(f"""
        <div class="score-hud">
            <div class="cyber-mono-label">ATS COMPATIBILITY MATCH</div>
            <div class="score-display-large">{score}%</div>
            <div class="score-hud-classification">
                MATCH CLASSIFICATION: <span class="status-badge {class_lower}">{classification} Match</span>
            </div>
            <div class="score-hud-meta">
                Your resume was audited against the job description. A score above 70% is recommended.
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    st.progress(score / 100.0)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # 2. PROFESSIONAL SUMMARY & ROLE PREDICTIONS (Unified Card)
    summary_bullets = results.get("professional_summary", [])
    if summary_bullets:
        bullet_html = "".join([f'<li class="cyber-list-item">{bullet}</li>' for bullet in summary_bullets])
    else:
        bullet_html = "<li style='color:#71717A;'>No summary generated.</li>"
        
    role_predictions = results.get("role_predictions", {})
    best_match = role_predictions.get("best_match", "N/A")
    alt_matches = role_predictions.get("alternative_matches", [])
    alt_roles = ", ".join(alt_matches) if alt_matches else "None predicted"
    
    summary_card_html = textwrap.dedent(f"""
    <div class="cyber-card">
        <div class="cyber-card-title">PROFESSIONAL SUMMARY</div>
        <div style="margin-bottom:1.25rem; font-size:0.88rem; color:#A1A1AA; line-height:1.5; background-color:#161616; padding:0.6rem 1rem; border:1px solid #1F1F1F; border-left:2px solid #FF3B30;">
            <span class="cyber-mono-label" style="color:#FF3B30; font-weight:700;">Best Fit Role:</span> <strong style="color:#FFFFFF;">{best_match}</strong>
            <span style="color:#333; margin: 0 10px;">|</span>
            <span class="cyber-mono-label" style="color:#A1A1AA; font-weight:700;">Alternative Fits:</span> <strong style="color:#FFFFFF;">{alt_roles}</strong>
        </div>
        <ul class="cyber-list">
            {bullet_html}
        </ul>
    </div>
    """)
    st.markdown(summary_card_html, unsafe_allow_html=True)

    # 3. CORE SKILLS & MISSING KEYWORDS
    col_skills, col_keywords = st.columns(2)
    
    with col_skills:
        # SECTION 5: CORE SKILLS
        extracted_skills = results.get("skills_extracted", [])
        if extracted_skills:
            chips_html = "".join([f'<span class="skill-chip">[ {skill} ]</span>' for skill in extracted_skills])
        else:
            chips_html = "<span style='color:#71717A;'>No predefined technical skills matched.</span>"
            
        skills_card_html = textwrap.dedent(f"""
        <div class="cyber-card">
            <div class="cyber-card-title">CORE SKILLS EXTRACTED</div>
            <div class="skills-wrapper">
                {chips_html}
            </div>
        </div>
        """)
        st.markdown(skills_card_html, unsafe_allow_html=True)
        
    with col_keywords:
        # SECTION 6: MISSING KEYWORDS
        missing_keywords = results.get("missing_keywords", [])
        if missing_keywords:
            keywords_html = "".join([f'<span class="keyword-chip">[ {kw} ]</span>' for kw in missing_keywords])
        else:
            keywords_html = "<span style='color:#22C55E; font-size:0.9rem;'>Perfect keyword coverage!</span>"
            
        keywords_card_html = textwrap.dedent(f"""
        <div class="cyber-card">
            <div class="cyber-card-title">MISSING KEYWORDS</div>
            <div class="keywords-wrapper">
                {keywords_html}
            </div>
        </div>
        """)
        st.markdown(keywords_card_html, unsafe_allow_html=True)

    # 4. RESUME HEALTH ANALYSIS & RECOMMENDED CORRECTIONS
    col_health, col_suggest = st.columns([2, 3])
    
    with col_health:
        # SECTION 6.5: RESUME HEALTH ANALYSIS
        health = results.get("health_analysis", {})
        health_score = health.get("health_score", 0)
        health_label = health.get("health_label", "Good")
        
        checklist_html = ""
        if "checklist" in health:
            checklist = health["checklist"]
            c_wc = "✅" if checklist.get("word_count") else "❌"
            c_sf = "✅" if checklist.get("sections_found") else "❌"
            c_sc = "✅" if checklist.get("skills_coverage") else "❌"
            c_af = "✅" if checklist.get("ats_formatting") else "❌"
            checklist_html = (
                f'<hr style="border-color:#1F1F1F; margin:1rem 0;"/>'
                f'<div style="font-size:0.85rem; line-height:1.6; color:#A1A1AA;">'
                f'<div>{c_wc} Length check</div>'
                f'<div>{c_sf} Key sections present</div>'
                f'<div>{c_sc} Skills representation</div>'
                f'<div>{c_af} Formatting index</div>'
                f'</div>'
            )
            
        health_card_html = (
            f'<div class="cyber-card">'
            f'<div class="cyber-card-title">RESUME HEALTH</div>'
            f'<div style="text-align:center; padding:0.5rem 0;">'
            f'<div style="font-size:3.5rem; font-family:\'Space Grotesk\'; font-weight:700; color:#FFFFFF; line-height:1;">{health_score}<span style="font-size:1.5rem; color:#71717A;">/100</span></div>'
            f'<div style="font-size:0.85rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; color:#FF3B30; margin-top:0.25rem;">{health_label} STATUS</div>'
            f'</div>'
            f'{checklist_html}'
            f'</div>'
        )
        st.markdown(health_card_html, unsafe_allow_html=True)
        
    with col_suggest:
        # SECTION 8: RECOMMENDED CORRECTIONS
        suggestions = results.get("improvement_suggestions", [])
        if suggestions:
            suggest_html = "".join([f'<li class="cyber-list-item">{s}</li>' for s in suggestions])
        else:
            suggest_html = "<span style='color:#22C55E;'>No corrections required.</span>"
            
        suggest_card_html = textwrap.dedent(f"""
        <div class="cyber-card">
            <div class="cyber-card-title">RECOMMENDED CORRECTIONS</div>
            <ul class="cyber-list">
                {suggest_html}
            </ul>
        </div>
        """)
        st.markdown(suggest_card_html, unsafe_allow_html=True)

    # SECTION 5: PDF REPORT EXPORT
    st.markdown("<br/>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### PDF Report Export")
        st.markdown(
            "Export the complete ATS compatibility analysis, role predictions, core skills, "
            "and recommended improvements into an offline-accessible, print-ready PDF audit report."
        )
        try:
            pdf_bytes = generate_pdf_report(results)
            st.download_button(
                label="DOWNLOAD PDF REPORT",
                data=pdf_bytes,
                file_name="AI_Resume_Audit_Report.pdf",
                mime="application/pdf"
            )
        except Exception as pdf_err:
            st.error(f"Error compiling PDF Report: {pdf_err}")

# SECTION 6: Advanced Settings (Main Page Expander - Always at the bottom)
st.markdown("<br/>", unsafe_allow_html=True)
with st.expander("⚙️ Advanced Settings", expanded=False):
    col_exp1, col_exp2 = st.columns([3, 1])
    with col_exp1:
        api_key_input = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            label_visibility="collapsed",
            placeholder="Enter Gemini API Key to enable AI analysis...",
            key="gemini_api_key"
        )
    with col_exp2:
        current_api_val = st.session_state.get("gemini_api_key", "").strip() or os.getenv("GEMINI_API_KEY", "")
        if current_api_val:
            st.markdown(
                '<div class="status-badge strong" style="display:block; text-align:center; height:42px; line-height:42px; box-sizing:border-box;">Gemini Engine</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="status-badge average" style="display:block; text-align:center; height:42px; line-height:42px; box-sizing:border-box;">Local Engine</div>',
                unsafe_allow_html=True
            )
