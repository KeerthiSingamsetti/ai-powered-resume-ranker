"""ui/pages/bias.py — Feature 5: JD Bias Detector (Premium UI)."""

import streamlit as st
from core.bias_detector import detect_bias


def render_bias_page():
    st.markdown('<div class="pg-heading">JD Bias Detector</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Scans the job description for age, gender, culture, and disability-biased language before screening starts</div>', unsafe_allow_html=True)

    jd = st.session_state.get("jd_text", "")

    if not jd.strip():
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📋</div><div class="empty-state-title">No job description</div><div class="empty-state-desc">Paste the JD in the section above to scan for biased language.</div></div>', unsafe_allow_html=True)
        return

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("⚖️  Scan for Bias", use_container_width=True)

    if run:
        with st.spinner("Scanning job description for biased language…"):
            st.session_state["bias_result"] = detect_bias(jd)

    result = st.session_state.get("bias_result")
    if not result:
        return

    counts     = result["severity_counts"]
    risk       = result["overall_risk"]
    risk_color = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#10b981"}[risk]
    risk_cls   = {"HIGH": "red", "MEDIUM": "amber", "LOW": "green"}[risk]

    # ── Metric Cards ───────────────────────────────────────────────────────────
    total_findings = len(result.get("findings", []))
    st.markdown(f"""
    <div class="metric-grid">
      <div class="m-card">
        <div class="m-card-label">Overall Risk</div>
        <div class="m-card-value {risk_cls}">{risk}</div>
        <div class="m-card-sub">bias severity level</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Total Findings</div>
        <div class="m-card-value">{total_findings}</div>
        <div class="m-card-sub">biased phrases found</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">High Severity</div>
        <div class="m-card-value red">{counts["HIGH"]}</div>
        <div class="m-card-sub">immediate attention</div>
      </div>
      <div class="m-card">
        <div class="m-card-label">Medium / Low</div>
        <div class="m-card-value amber">{counts["MEDIUM"] + counts["LOW"]}</div>
        <div class="m-card-sub">review suggested</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Clean or Found ─────────────────────────────────────────────────────────
    if result["bias_free"]:
        st.markdown("""
        <div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.2);
             border-radius:14px;padding:1.4rem 1.8rem;color:#34d399;font-weight:600;
             display:flex;align-items:center;gap:0.8rem;font-family:'Inter',sans-serif;">
            <span style="font-size:1.5rem;">✅</span>
            <div>
                <div style="font-size:1rem;font-weight:700;font-family:'Outfit',sans-serif;">JD Looks Inclusive!</div>
                <div style="font-size:0.83rem;color:#6ee7b7;margin-top:0.2rem;">
                    No biased language detected — this job description appears fair and inclusive.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);
         border-radius:14px;padding:1.1rem 1.5rem;color:#fca5a5;font-size:0.88rem;
         margin-bottom:1.4rem;font-family:'Inter',sans-serif;display:flex;align-items:center;gap:0.7rem;">
        <span style="font-size:1.3rem;">⚠️</span>
        <div>
            <strong style="font-family:'Outfit',sans-serif;">{total_findings} biased phrase(s) detected.</strong>
            Update the job description before posting to attract a diverse candidate pool.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Findings Cards ─────────────────────────────────────────────────────────
    sev_cls_map = {"HIGH": "sev-high", "MEDIUM": "sev-med", "LOW": "sev-low"}

    for i, f in enumerate(result["findings"]):
        sev_cls = sev_cls_map.get(f["severity"], "sev-low")
        st.markdown(f"""
        <div class="bias-card {sev_cls}" style="animation-delay:{i*0.07}s;">
            <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.6rem;">
                <span class="sev-{f['severity']}">{f['severity']}</span>
                <span style="font-size:0.75rem;color:#64748b;font-family:'Inter',sans-serif;">
                    {f['category']}
                </span>
            </div>
            <div style="font-size:0.95rem;font-weight:700;color:#fbbf24;
                        font-family:'Outfit',sans-serif;margin-bottom:0.3rem;">
                "{f['phrase']}"
            </div>
            <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.5rem;
                        font-family:'Inter',sans-serif;font-style:italic;">
                Context: …{f['context'][:110]}…
            </div>
            <div style="font-size:0.82rem;color:#6ee7b7;font-family:'Inter',sans-serif;
                        display:flex;align-items:flex-start;gap:0.4rem;">
                <span>💡</span>
                <span>{f['suggestion']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
