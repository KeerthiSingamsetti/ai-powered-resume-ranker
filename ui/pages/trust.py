"""ui/pages/trust.py — Feature 3: Trust Score (SVG Ring Gauge)."""

import streamlit as st
import streamlit.components.v1 as components
from core.trust_score import compute_trust_score


def _svg_ring(score: int, color: str) -> str:
    radius    = 70
    stroke    = 10
    cx = cy   = 90
    circumf   = 2 * 3.14159 * radius
    filled    = (score / 100) * circumf
    dash_arr  = f"{filled:.1f} {circumf:.1f}"
    track_col = "rgba(30,41,59,0.9)"
    gid       = f"ring-grad-{score}"
    offset    = f"{circumf * 0.25:.1f}"

    return (
        f'<svg width="180" height="180" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg" style="pointer-events:none;">'
        f'<defs>'
        f'<linearGradient id="{gid}" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{color}" stop-opacity="1"/>'
        f'<stop offset="100%" stop-color="{color}" stop-opacity="0.5"/>'
        f'</linearGradient>'
        f'<filter id="glow{score}">'
        f'<feGaussianBlur stdDeviation="3" result="blur"/>'
        f'<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f'</filter>'
        f'</defs>'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{track_col}" stroke-width="{stroke}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="url(#{gid})" '
        f'stroke-width="{stroke}" stroke-linecap="round" '
        f'stroke-dasharray="{dash_arr}" stroke-dashoffset="{offset}" filter="url(#glow{score})"/>'
        f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" '
        f'font-family="Outfit,sans-serif" font-size="32" font-weight="900" fill="{color}">{score}</text>'
        f'<text x="{cx}" y="{cy + 16}" text-anchor="middle" '
        f'font-family="Inter,sans-serif" font-size="11" fill="#475569" font-weight="600">/ 100</text>'
        f'</svg>'
    )


def render_trust_page():
    st.markdown('<div class="pg-heading">Trust Score — Authenticity Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Detects fake experience claims, unexplained employment gaps, and suspicious job-hopping patterns</div>', unsafe_allow_html=True)

    resumes = st.session_state.get("resumes", [])
    if not resumes:
        st.markdown(
            '<div class="empty-state">'
            '<div class="empty-state-icon">📭</div>'
            '<div class="empty-state-title">No resumes uploaded</div>'
            '<div class="empty-state-desc">Upload PDF resumes above to analyze trust scores.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        return

    candidate = st.selectbox(
        "Select candidate",
        [r["name"] for r in resumes],
        label_visibility="collapsed",
        key="trust_candidate_select"
    )
    resume = next(r for r in resumes if r["name"] == candidate)

    with st.spinner("Computing trust score…"):
        result = compute_trust_score(resume["text"])

    score = result["score"]
    if score >= 75:
        color   = "#10b981"
        verdict = "✓ Trustworthy Candidate"
    elif score >= 50:
        color   = "#f59e0b"
        verdict = "⚠ Moderate Risk Detected"
    else:
        color   = "#ef4444"
        verdict = "✗ High Risk — Review Carefully"

    col_ring, col_detail = st.columns([1, 2], gap="large")

    with col_ring:
        ring_html = _svg_ring(score, color)
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: 'Inter', sans-serif;
            }}
            .trust-panel {{
                background: rgba(11,15,36,0.8);
                border: 1px solid rgba(30,41,59,0.9);
                border-radius: 20px;
                padding: 2rem 1.5rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }}
            .trust-verdict {{
                font-size: 1rem;
                font-weight: 700;
                margin-top: 0.8rem;
                font-family: 'Outfit', sans-serif;
                color: {color};
            }}
            .trust-score-label {{
                font-size: 0.72rem;
                color: #475569;
                font-family: 'Inter', sans-serif;
                margin-top: 0.4rem;
                letter-spacing: 0.05em;
                text-transform: uppercase;
            }}
        </style>
        </head>
        <body>
            <div class="trust-panel">
                {ring_html}
                <div class="trust-verdict">{verdict}</div>
                <div class="trust-score-label">Authenticity Rating</div>
            </div>
        </body>
        </html>
        """
        components.html(full_html, height=320)

    with col_detail:
        grad_yr = result["graduation_year"] or "—"
        claimed = f"{result['claimed_exp']} yrs" if result["claimed_exp"] else "—"
        actual  = f"{result['actual_exp_years']} yrs"

        st.markdown(
            '<div class="metric-grid-3">'
            '<div class="m-card"><div class="m-card-label">Graduation Year</div>'
            f'<div class="m-card-value purple">{grad_yr}</div>'
            '<div class="m-card-sub">from resume</div></div>'
            '<div class="m-card"><div class="m-card-label">Claimed Exp</div>'
            f'<div class="m-card-value">{claimed}</div>'
            '<div class="m-card-sub">stated in resume</div></div>'
            '<div class="m-card"><div class="m-card-label">Actual Exp</div>'
            f'<div class="m-card-value green">{actual}</div>'
            '<div class="m-card-sub">calculated from dates</div></div>'
            '</div>',
            unsafe_allow_html=True
        )

        if result["red_flags"]:
            st.markdown(
                '<div class="skill-section-label" style="color:#f87171;">🚩 Red Flags Detected</div>',
                unsafe_allow_html=True
            )
            for flag in result["red_flags"]:
                st.markdown(
                    f'<div class="flag-row">{flag}</div>',
                    unsafe_allow_html=True
                )

        st.write("")

        if result["positives"]:
            st.markdown(
                '<div class="skill-section-label" style="color:#34d399;">✅ Positive Signals</div>',
                unsafe_allow_html=True
            )
            for p in result["positives"]:
                st.markdown(
                    f'<div class="ok-row">{p}</div>',
                    unsafe_allow_html=True
                )