"""
app.py — AI-Powered Resume Ranker | HR Intelligence Platform
Run: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="AI Resume Ranker | HR Intelligence Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from ui.styles import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

from ui.pages.ranking    import render_ranking_page
from ui.pages.skill_gap  import render_skill_gap_page
from ui.pages.trust      import render_trust_page
from ui.pages.radar      import render_radar_page
from ui.pages.bias       import render_bias_page
from ui.pages.interview  import render_interview_page
from ui.pages.comparison import render_comparison_page

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in {
    "resumes":      [],
    "ranked":       [],
    "jd_text":      "",
    "claude_key":   "",
    "upload_done":  False,
    "bias_result":  None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">
    <span class="hero-eyebrow-dot"></span>
    AI · NLP · HR Intelligence Platform
  </div>
  <h1 class="hero-title">
    Resume Ranker
    <span class="hero-title-accent">Powered by AI</span>
  </h1>
  <p class="hero-desc">
    Upload resumes &amp; a job description — get instant AI-powered rankings,<br>
    skill gap analysis, trust verification, bias detection &amp; smart interview questions.
  </p>
  <div class="hero-stats-row">
    <div class="hero-stat">
      <div class="hero-stat-num">80%</div>
      <div class="hero-stat-label">Time Saved</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-num">6</div>
      <div class="hero-stat-label">AI Features</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-num">100%</div>
      <div class="hero-stat-label">Bias-Aware</div>
    </div>
    <div class="hero-stat">
      <div class="hero-stat-num">NLP</div>
      <div class="hero-stat-label">Powered Engine</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── How It Works ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-wrap">
  <div class="step-card">
    <div class="step-icon-wrap">📄</div>
    <div>
      <div class="step-num">Step 01</div>
      <div class="step-title">Upload &amp; Configure</div>
      <div class="step-desc">Upload PDF resumes and paste the job description to begin analysis.</div>
    </div>
  </div>
  <div class="step-card">
    <div class="step-icon-wrap">🧠</div>
    <div>
      <div class="step-num">Step 02</div>
      <div class="step-title">AI Analysis</div>
      <div class="step-desc">TF-IDF, Cosine Similarity, NLP, and Claude AI process everything instantly.</div>
    </div>
  </div>
  <div class="step-card">
    <div class="step-icon-wrap">📊</div>
    <div>
      <div class="step-num">Step 03</div>
      <div class="step-title">Review &amp; Export</div>
      <div class="step-desc">Get ranked leaderboards, skill gaps, trust scores, and interview questions.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-label">Step 1 — Upload &amp; Configure</div>
""", unsafe_allow_html=True)

col_upload, col_jd = st.columns([1, 1], gap="large")

with col_upload:
    with st.container(border=True):
        st.markdown('<div class="input-card-title">📄 Upload Resumes <span class="badge-pill">PDF</span></div>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Drop PDF resumes here",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        if uploaded_files:
            from core.resume_parser import extract_text_from_pdf
            resumes = []
            for f in uploaded_files:
                text = extract_text_from_pdf(f)
                resumes.append({"name": f.name.replace(".pdf", ""), "text": text})
            st.session_state.resumes = resumes
            st.session_state.upload_done = True

with col_jd:
    with st.container(border=True):
        st.markdown('<div class="input-card-title">📋 Job Description</div>', unsafe_allow_html=True)
        
        jd_input_mode = st.radio(
            "JD Input Mode",
            options=["Paste Text", "Upload PDF"],
            horizontal=True,
            label_visibility="collapsed",
            key="jd_input_mode_selector"
        )
        
        jd_text = ""
        
        if jd_input_mode == "Paste Text":
            jd_pasted = st.text_area(
                "Paste JD",
                value=st.session_state.get("jd_pasted_text", ""),
                height=110,
                placeholder="Paste the full job description here — roles, requirements, skills...",
                label_visibility="collapsed",
                key="jd_pasted_area"
            )
            st.session_state.jd_pasted_text = jd_pasted
            jd_text = jd_pasted
        else:
            uploaded_jd_file = st.file_uploader(
                "Upload JD PDF",
                type=["pdf"],
                label_visibility="collapsed",
                key="jd_file_uploader"
            )
            if uploaded_jd_file:
                from core.resume_parser import extract_text_from_pdf
                file_key = f"jd_pdf_text_{uploaded_jd_file.name}"
                if file_key not in st.session_state:
                    with st.spinner("Extracting text from JD PDF..."):
                        extracted_jd_text = extract_text_from_pdf(uploaded_jd_file)
                        st.session_state[file_key] = extracted_jd_text
                jd_text = st.session_state[file_key]
        
        st.session_state.jd_text = jd_text
        if jd_text.strip():
            word_count = len(jd_text.split())
            char_count = len(jd_text)
            st.markdown(f'<div class="jd-meta">✓ {word_count} words · {char_count} characters loaded</div>', unsafe_allow_html=True)

# ── Stats Summary Banner (shown after ranking is done) ─────────────────────────
ranked = st.session_state.get("ranked", [])
resumes = st.session_state.get("resumes", [])

if ranked:
    top_score   = ranked[0]["match_score"]
    avg_score   = sum(r["match_score"] for r in ranked) / len(ranked)
    bottom_score= ranked[-1]["match_score"]
    top_name    = ranked[0]["name"]
    count       = len(ranked)

    top_color   = "green" if top_score >= 70 else "amber" if top_score >= 40 else "red"
    avg_color   = "blue"
    bias_result = st.session_state.get("bias_result")
    bias_risk   = bias_result["overall_risk"] if bias_result else "—"
    bias_color  = "red" if bias_risk == "HIGH" else "amber" if bias_risk == "MEDIUM" else "green" if bias_risk == "LOW" else "purple"

    st.markdown(f"""
    <div class="stats-banner">
      <div class="stat-card {top_color}">
        <div class="stat-card-label">Top Match</div>
        <div class="stat-card-value">{top_score:.1f}%</div>
        <div class="stat-card-sub">{top_name[:22]}</div>
      </div>
      <div class="stat-card {avg_color}">
        <div class="stat-card-label">Average Score</div>
        <div class="stat-card-value">{avg_score:.1f}%</div>
        <div class="stat-card-sub">Across {count} candidate{'s' if count != 1 else ''}</div>
      </div>
      <div class="stat-card purple">
        <div class="stat-card-label">Screened</div>
        <div class="stat-card-value">{count}</div>
        <div class="stat-card-sub">Resumes analyzed</div>
      </div>
      <div class="stat-card {bias_color}">
        <div class="stat-card-label">Bias Risk</div>
        <div class="stat-card-value">{bias_risk}</div>
        <div class="stat-card-sub">JD scan result</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS — 7 FEATURES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-label">Step 2 — Analyze</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏆  Ranking",
    "🔍  Skill Gap",
    "🛡️  Trust Score",
    "📡  Radar Chart",
    "⚖️  Bias Detector",
    "🤖  Interview AI",
    "📊  Comparison",
])

with tab1: render_ranking_page()
with tab2: render_skill_gap_page()
with tab3: render_trust_page()
with tab4: render_radar_page()
with tab5: render_bias_page()
with tab6: render_interview_page()
with tab7: render_comparison_page()
