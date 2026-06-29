"""ui/pages/skill_gap.py — Feature 2: Skill Gap Analyzer (Premium UI)."""

import streamlit as st
from core.skill_gap import analyze_skill_gap


def _tags(skills, cls, icon=""):
    return "".join(
        f'<span class="stag {cls}">{icon} {s}</span>'
        for s in sorted(skills)
    )


def render_skill_gap_page():
    st.markdown('<div class="pg-heading">Skill Gap Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Shows exactly which JD skills are matched, missing, or bonus for each candidate</div>', unsafe_allow_html=True)

    resumes = st.session_state.get("resumes", [])
    jd      = st.session_state.get("jd_text", "")

    if not resumes:
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-title">No resumes uploaded</div><div class="empty-state-desc">Upload PDF resumes above to analyze skill gaps.</div></div>', unsafe_allow_html=True)
        return
    if not jd.strip():
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📋</div><div class="empty-state-title">No job description</div><div class="empty-state-desc">Paste the JD above to compare skills.</div></div>', unsafe_allow_html=True)
        return

    candidate = st.selectbox("Select candidate", [r["name"] for r in resumes], label_visibility="collapsed", key="skill_gap_candidate_select")
    resume    = next(r for r in resumes if r["name"] == candidate)
    result    = analyze_skill_gap(resume["text"], jd)

    pct       = result["match_pct"]
    bar_col   = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
    pct_color = "green" if pct >= 70 else "amber" if pct >= 40 else "red"
    pct_lbl   = "Excellent" if pct >= 70 else "Moderate" if pct >= 40 else "Low"

    # ── Metric Cards ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="metric-grid">
      <div class="m-card">
        <div class="m-card-label">JD Skills Required</div>
        <div class="m-card-value">{len(result["jd_skills"])}</div>
        <div class="m-card-sub">from job description</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Matched ✓</div>
        <div class="m-card-value green">{len(result["matched"])}</div>
        <div class="m-card-sub">skills found in resume</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Missing ✗</div>
        <div class="m-card-value red">{len(result["missing"])}</div>
        <div class="m-card-sub">skills not found</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Bonus ★</div>
        <div class="m-card-value purple">{len(result["extra"])}</div>
        <div class="m-card-sub">extra skills in resume</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Donut Match Bar ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="donut-wrap">
      <svg width="80" height="80" viewBox="0 0 80 80">
        <defs>
          <linearGradient id="donut-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{bar_col}"/>
            <stop offset="100%" stop-color="{bar_col}" stop-opacity="0.5"/>
          </linearGradient>
        </defs>
        <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(30,41,59,0.9)" stroke-width="8"/>
        <circle cx="40" cy="40" r="32" fill="none"
                stroke="url(#donut-grad)" stroke-width="8"
                stroke-linecap="round"
                stroke-dasharray="{(pct/100)*201.1:.1f} 201.1"
                stroke-dashoffset="50.3"
                style="transition:stroke-dasharray 1s ease;"/>
        <text x="40" y="44" text-anchor="middle" font-family="Outfit,sans-serif"
              font-size="13" font-weight="900" fill="{bar_col}">{pct:.0f}%</text>
      </svg>
      <div class="donut-info">
        <div class="donut-pct" style="color:{bar_col};">{pct:.1f}%</div>
        <div class="donut-label">Skill Match Rate — <strong>{pct_lbl}</strong></div>
        <div class="match-bar-outer">
          <div class="match-bar-inner" style="width:{pct}%;background:linear-gradient(90deg,{bar_col},{bar_col}88);"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Skill Tags ─────────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        if result["matched"]:
            st.markdown('<div class="skill-section-label" style="color:#34d399;">✓ MATCHED SKILLS</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="skill-wrap">{_tags(result["matched"], "stag-match", "✓")}</div>', unsafe_allow_html=True)

        if result["extra"]:
            st.markdown('<div class="skill-section-label" style="color:#a5b4fc;">★ BONUS SKILLS</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="skill-wrap">{_tags(result["extra"], "stag-extra", "★")}</div>', unsafe_allow_html=True)

    with col_b:
        if result["missing"]:
            st.markdown('<div class="skill-section-label" style="color:#f87171;">✗ MISSING SKILLS</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="skill-wrap">{_tags(result["missing"], "stag-missing", "✗")}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="ok-row">✓ All JD skills are present in this resume — perfect match!</div>', unsafe_allow_html=True)
