"""ui/pages/comparison.py — Feature 7: Candidate Comparison Table (New)."""

import streamlit as st
from core.skill_gap   import analyze_skill_gap
from core.trust_score import compute_trust_score


def render_comparison_page():
    st.markdown('<div class="pg-heading">Candidate Comparison Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Side-by-side comparison of all candidates across every metric — ranked, colored, and exportable</div>', unsafe_allow_html=True)

    resumes = st.session_state.get("resumes", [])
    ranked  = st.session_state.get("ranked", [])
    jd      = st.session_state.get("jd_text", "")

    if not resumes:
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📊</div><div class="empty-state-title">No resumes uploaded</div><div class="empty-state-desc">Upload PDF resumes above to see the comparison table.</div></div>', unsafe_allow_html=True)
        return
    if not jd.strip():
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📋</div><div class="empty-state-title">No job description</div><div class="empty-state-desc">Paste the JD above to enable skill gap comparison.</div></div>', unsafe_allow_html=True)
        return

    col_btn, _ = st.columns([1.2, 4])
    with col_btn:
        run = st.button("📊  Build Comparison", use_container_width=True)

    if not run and "comp_data" not in st.session_state:
        return

    if run:
        rows = []
        with st.spinner("Analyzing all candidates…"):
            for r in resumes:
                # Get rank & score
                ranked_r    = next((x for x in ranked if x["name"] == r["name"]), None)
                match_score = ranked_r["match_score"] if ranked_r else None
                rank_pos    = ranked_r["rank"] if ranked_r else "—"

                # Skill gap
                gap = analyze_skill_gap(r["text"], jd)
                matched_cnt = len(gap["matched"])
                missing_cnt = len(gap["missing"])
                bonus_cnt   = len(gap["extra"])
                skill_pct   = gap["match_pct"]

                # Trust
                trust       = compute_trust_score(r["text"])
                trust_score = trust["score"]
                flags_cnt   = len(trust["red_flags"])

                rows.append({
                    "rank":         rank_pos,
                    "name":         r["name"],
                    "match_score":  match_score,
                    "skill_pct":    skill_pct,
                    "matched":      matched_cnt,
                    "missing":      missing_cnt,
                    "bonus":        bonus_cnt,
                    "trust_score":  trust_score,
                    "red_flags":    flags_cnt,
                })

        # Sort by match_score if available, else by name
        rows.sort(key=lambda x: x["match_score"] if x["match_score"] is not None else -1, reverse=True)
        st.session_state["comp_data"] = rows

    rows = st.session_state.get("comp_data", [])
    if not rows:
        return

    # ── Summary metrics ────────────────────────────────────────────────────────
    scores_only = [r["match_score"] for r in rows if r["match_score"] is not None]
    best_match  = max(scores_only) if scores_only else 0
    avg_match   = (sum(scores_only) / len(scores_only)) if scores_only else 0
    avg_trust   = sum(r["trust_score"] for r in rows) / len(rows)
    total_flags = sum(r["red_flags"] for r in rows)

    st.markdown(f"""
    <div class="metric-grid">
      <div class="m-card">
        <div class="m-card-label">Candidates</div>
        <div class="m-card-value">{len(rows)}</div>
        <div class="m-card-sub">total compared</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Best Match</div>
        <div class="m-card-value green">{best_match:.1f}%</div>
        <div class="m-card-sub">top candidate score</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Avg Trust Score</div>
        <div class="m-card-value {'green' if avg_trust>=75 else 'amber' if avg_trust>=50 else 'red'}">{avg_trust:.0f}</div>
        <div class="m-card-sub">pool average</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Total Red Flags</div>
        <div class="m-card-value {'green' if total_flags==0 else 'amber' if total_flags<=3 else 'red'}">{total_flags}</div>
        <div class="m-card-sub">across all candidates</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Comparison Table ───────────────────────────────────────────────────────
    cols_def = "2fr 1fr 1fr 1fr 1fr 1fr 1fr"

    st.markdown(f"""
    <div class="comp-table-wrap">
      <div class="comp-table-head" style="grid-template-columns:{cols_def};">
        <span>Candidate</span>
        <span style="text-align:center;">Rank</span>
        <span style="text-align:center;">Match %</span>
        <span style="text-align:center;">Skill Fit</span>
        <span style="text-align:center;">Missing</span>
        <span style="text-align:center;">Trust</span>
        <span style="text-align:center;">Red Flags</span>
      </div>
    """, unsafe_allow_html=True)

    MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}

    for i, row in enumerate(rows):
        rank_display   = MEDALS.get(row["rank"], f"#{row['rank']}" if row["rank"] != "—" else "—")
        match_disp     = f"{row['match_score']:.1f}%" if row["match_score"] is not None else "—"
        match_col      = "#34d399" if (row["match_score"] or 0) >= 70 else "#fbbf24" if (row["match_score"] or 0) >= 40 else "#f87171"
        skill_col      = "#34d399" if row["skill_pct"] >= 70 else "#fbbf24" if row["skill_pct"] >= 40 else "#f87171"
        trust_col      = "#34d399" if row["trust_score"] >= 75 else "#fbbf24" if row["trust_score"] >= 50 else "#f87171"
        flag_col       = "#34d399" if row["red_flags"] == 0 else "#fbbf24" if row["red_flags"] <= 2 else "#f87171"

        st.markdown(f"""
        <div class="comp-table-row" style="grid-template-columns:{cols_def};">
          <div class="comp-name">{row['name']}</div>
          <div class="comp-cell" style="color:#a5b4fc;">{rank_display}</div>
          <div class="comp-cell" style="color:{match_col};">{match_disp}</div>
          <div class="comp-cell" style="color:{skill_col};">{row['skill_pct']:.1f}%</div>
          <div class="comp-cell" style="color:{('#f87171' if row['missing']>0 else '#34d399')};">{row['missing']}</div>
          <div class="comp-cell" style="color:{trust_col};">{row['trust_score']}</div>
          <div class="comp-cell" style="color:{flag_col};">{row['red_flags']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Legend ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;gap:1.5rem;flex-wrap:wrap;font-size:0.72rem;
                font-family:'Inter',sans-serif;color:#475569;">
      <span>🟢 <strong style="color:#34d399;">Green</strong> = Strong</span>
      <span>🟡 <strong style="color:#fbbf24;">Amber</strong> = Moderate</span>
      <span>🔴 <strong style="color:#f87171;">Red</strong> = Weak / Risk</span>
      <span style="color:#334155;">· Match %: TF-IDF cosine similarity · Skill Fit: JD skill overlap · Trust: authenticity score</span>
    </div>
    """, unsafe_allow_html=True)
