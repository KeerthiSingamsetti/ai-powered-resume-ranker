"""ui/pages/ranking.py — Feature 1: Multi-Resume Ranking (Premium UI)."""

import io
import csv
import streamlit as st
from core.ranker import rank_resumes


def _empty(msg, desc, icon="📭"):
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{msg}</div>
        <div class="empty-state-desc">{desc}</div>
    </div>""", unsafe_allow_html=True)


def render_ranking_page():
    st.markdown('<div class="pg-heading">Resume Ranking Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">TF-IDF + Cosine Similarity ranks every resume against the job description in real-time</div>', unsafe_allow_html=True)

    resumes = st.session_state.get("resumes", [])
    jd      = st.session_state.get("jd_text", "")

    if not resumes:
        _empty("No resumes uploaded", "Upload PDF resumes in the section above to get started.", "📭")
        return
    if not jd.strip():
        _empty("No job description", "Paste the job description in the section above.", "📋")
        return

    col_btn, col_dl, col_space = st.columns([1.2, 1.2, 3])
    with col_btn:
        run = st.button("▶  Run Analysis", use_container_width=True)

    if run:
        with st.spinner("Analyzing resumes with TF-IDF…"):
            st.session_state.ranked = rank_resumes(resumes, jd)

    ranked = st.session_state.get("ranked", [])
    if not ranked:
        return

    # ── CSV Export ─────────────────────────────────────────────────────────────
    with col_dl:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Rank", "Name", "Match Score (%)"])
        for r in ranked:
            writer.writerow([r["rank"], r["name"], f"{r['match_score']:.1f}"])
        csv_bytes = output.getvalue().encode()
        st.download_button(
            label="⬇  Export CSV",
            data=csv_bytes,
            file_name="resume_rankings.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ── Custom Metric Cards ────────────────────────────────────────────────────
    avg_score = sum(r["match_score"] for r in ranked) / len(ranked)
    top_score = ranked[0]["match_score"]
    bot_score = ranked[-1]["match_score"]
    spread    = top_score - bot_score

    top_color = "green" if top_score >= 70 else "amber" if top_score >= 40 else "red"
    avg_color = "purple" if avg_score >= 60 else "amber" if avg_score >= 35 else "red"

    st.markdown(f"""
    <div class="metric-grid">
      <div class="m-card">
        <div class="m-card-label">Resumes Analyzed</div>
        <div class="m-card-value">{len(ranked)}</div>
        <div class="m-card-sub">candidates screened</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Top Match</div>
        <div class="m-card-value {top_color}">{top_score:.1f}%</div>
        <div class="m-card-sub">{ranked[0]['name'][:20]}</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Average Score</div>
        <div class="m-card-value {avg_color}">{avg_score:.1f}%</div>
        <div class="m-card-sub">pool average</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Score Spread</div>
        <div class="m-card-value">{spread:.1f}%</div>
        <div class="m-card-sub">top vs bottom gap</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Leaderboard ────────────────────────────────────────────────────────────
    MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}
    MEDAL_CLASSES = {1: "gold", 2: "silver", 3: "bronze"}

    for r in ranked:
        rank    = r["rank"]
        pos     = MEDALS.get(rank, f"#{rank}")
        score   = r["match_score"]
        cls     = MEDAL_CLASSES.get(rank, "")

        if score >= 70:
            bar_color   = "linear-gradient(90deg, #10b981, #34d399)"
            score_color = "#34d399"
            status_tag  = "Strong Match"
        elif score >= 40:
            bar_color   = "linear-gradient(90deg, #f59e0b, #fbbf24)"
            score_color = "#fbbf24"
            status_tag  = "Moderate Match"
        else:
            bar_color   = "linear-gradient(90deg, #ef4444, #f87171)"
            score_color = "#f87171"
            status_tag  = "Weak Match"

        st.markdown(f"""
        <div class="rank-row {cls}">
            <div class="rank-pos">{pos}</div>
            <div class="rank-info">
                <div class="rank-name">{r['name']}</div>
                <div class="rank-tag">{status_tag}</div>
                <div class="rank-bar-bg">
                    <div class="rank-bar-fill" style="width:{score:.0f}%;background:{bar_color};"></div>
                </div>
            </div>
            <div class="rank-pct" style="color:{score_color};">{score:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
