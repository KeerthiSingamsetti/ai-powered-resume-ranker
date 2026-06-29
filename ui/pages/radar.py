"""ui/pages/radar.py — Feature 4: Radar Chart Comparison (Premium UI)."""

import streamlit as st
from core.radar_chart import build_candidate_dimensions, create_radar_chart
from core.trust_score import compute_trust_score


def render_radar_page():
    st.markdown('<div class="pg-heading">Radar Comparison Chart</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Interactive spider chart comparing top candidates across 6 key dimensions using Plotly</div>', unsafe_allow_html=True)

    resumes = st.session_state.get("resumes", [])
    ranked  = st.session_state.get("ranked", [])

    if not resumes:
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-title">No resumes uploaded</div><div class="empty-state-desc">Upload PDF resumes above to start comparison.</div></div>', unsafe_allow_html=True)
        return
    if len(resumes) < 2:
        st.markdown('<div class="empty-state"><div class="empty-state-icon">👥</div><div class="empty-state-title">Need at least 2 resumes</div><div class="empty-state-desc">Upload 2 or more PDF resumes to enable radar comparison.</div></div>', unsafe_allow_html=True)
        return

    all_names = [r["name"] for r in resumes]
    selected  = st.multiselect(
        "Select candidates to compare (max 3)",
        all_names,
        default=all_names[:min(3, len(all_names))],
        max_selections=3,
        label_visibility="collapsed",
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("📡  Generate Chart", use_container_width=True)

    if run and selected:
        with st.spinner("Building radar comparison chart…"):
            candidates_data = []
            for name in selected:
                resume   = next(r for r in resumes if r["name"] == name)
                ranked_r = next((r for r in ranked if r["name"] == name), {"match_score": 0})
                trust    = compute_trust_score(resume["text"])
                dim      = build_candidate_dimensions(
                    {"name": name, "text": resume["text"], "match_score": ranked_r.get("match_score", 0)},
                    trust,
                )
                candidates_data.append(dim)

            fig = create_radar_chart(candidates_data)
            st.plotly_chart(fig, use_container_width=True)

            # ── Dimension comparison table ──────────────────────────────────────
            st.divider()
            dims = ["Technical Skills", "Experience Depth", "Trust Score",
                    "Skill Match %", "Certifications", "Soft Skills"]

            # Header
            header_cols = st.columns([2] + [1]*len(candidates_data))
            header_cols[0].markdown('<div style="font-size:0.68rem;color:#475569;font-weight:800;letter-spacing:0.12em;text-transform:uppercase;font-family:Inter,sans-serif;">DIMENSION</div>', unsafe_allow_html=True)
            for i, cd in enumerate(candidates_data):
                header_cols[i+1].markdown(f'<div style="font-size:0.78rem;color:#818cf8;font-weight:700;text-align:center;font-family:Outfit,sans-serif;">{cd["name"]}</div>', unsafe_allow_html=True)

            st.markdown('<hr style="margin:0.5rem 0 0.75rem;">', unsafe_allow_html=True)

            for j, dim in enumerate(dims):
                row_cols = st.columns([2] + [1]*len(candidates_data))
                row_cols[0].markdown(f'<div style="font-size:0.83rem;color:#94a3b8;padding:5px 0;font-family:Inter,sans-serif;">{dim}</div>', unsafe_allow_html=True)
                for i, cd in enumerate(candidates_data):
                    val = cd["scores"][j]
                    color = "#34d399" if val >= 70 else "#fbbf24" if val >= 40 else "#f87171"
                    row_cols[i+1].markdown(
                        f'<div style="font-size:0.95rem;font-weight:800;color:{color};'
                        f'text-align:center;padding:5px 0;font-family:Outfit,sans-serif;">{val:.0f}</div>',
                        unsafe_allow_html=True
                    )
