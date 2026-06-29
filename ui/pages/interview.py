"""ui/pages/interview.py — Feature 6: AI Interview Question Generator (Premium UI)."""

import streamlit as st
from core.interview_gen import generate_interview_questions
from core.skill_gap     import analyze_skill_gap


def render_interview_page():
    st.markdown('<div class="pg-heading">AI Interview Question Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Generates 5 personalized interview questions per candidate using Claude AI — tailored to skill gaps</div>', unsafe_allow_html=True)

    resumes = st.session_state.get("resumes", [])
    jd      = st.session_state.get("jd_text", "")

    if not resumes:
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📭</div><div class="empty-state-title">No resumes uploaded</div><div class="empty-state-desc">Upload PDF resumes above to generate interview questions.</div></div>', unsafe_allow_html=True)
        return
    if not jd.strip():
        st.markdown('<div class="empty-state"><div class="empty-state-icon">📋</div><div class="empty-state-title">No job description</div><div class="empty-state-desc">Paste the JD above to create targeted questions.</div></div>', unsafe_allow_html=True)
        return

    # ── Config row ─────────────────────────────────────────────────────────────
    col_cand, col_key = st.columns([1, 1], gap="large")

    with col_cand:
        st.markdown('<div class="skill-section-label" style="color:#94a3b8;">SELECT CANDIDATE</div>', unsafe_allow_html=True)
        candidate = st.selectbox("Candidate", [r["name"] for r in resumes], label_visibility="collapsed", key="interview_candidate_select")

    with col_key:
        st.markdown('<div class="skill-section-label" style="color:#94a3b8;">CLAUDE API KEY</div>', unsafe_allow_html=True)
        api_key = st.text_input(
            "Claude API key",
            value=st.session_state.get("claude_key", ""),
            type="password",
            placeholder="sk-ant-api03-…",
            label_visibility="collapsed",
        )
        if api_key:
            st.session_state.claude_key = api_key

    resume  = next(r for r in resumes if r["name"] == candidate)
    gap     = analyze_skill_gap(resume["text"], jd)
    missing = list(gap["missing"])

    # ── Candidate context card ─────────────────────────────────────────────────
    missing_str = ", ".join(sorted(missing)[:6]) if missing else "None identified"
    matched_pct = gap["match_pct"]
    pct_color   = "#34d399" if matched_pct >= 70 else "#fbbf24" if matched_pct >= 40 else "#f87171"

    st.markdown(f"""
    <div style="background:rgba(11,15,36,0.8);border:1px solid rgba(30,41,59,0.9);
         border-radius:14px;padding:1.2rem 1.5rem;display:flex;gap:2.5rem;
         align-items:center;margin:1.2rem 0;backdrop-filter:blur(10px);flex-wrap:wrap;">
        <div>
            <div style="font-size:0.65rem;color:#475569;font-weight:700;
                        letter-spacing:.12em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Candidate
            </div>
            <div style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-top:3px;
                        font-family:'Outfit',sans-serif;">{candidate}</div>
        </div>
        <div>
            <div style="font-size:0.65rem;color:#475569;font-weight:700;
                        letter-spacing:.12em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Skill Match
            </div>
            <div style="font-size:1.1rem;font-weight:800;color:{pct_color};margin-top:3px;
                        font-family:'Outfit',sans-serif;">{matched_pct:.1f}%</div>
        </div>
        <div style="flex:1;min-width:180px;">
            <div style="font-size:0.65rem;color:#475569;font-weight:700;
                        letter-spacing:.12em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Skills to Probe
            </div>
            <div style="font-size:0.85rem;color:#f87171;margin-top:3px;
                        font-family:'Inter',sans-serif;">{missing_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── API Key notice ─────────────────────────────────────────────────────────
    if not api_key:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.2);
             border-radius:12px;padding:1rem 1.3rem;color:#fbbf24;font-size:0.85rem;
             font-family:'Inter',sans-serif;display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1.2rem;">🔑</span>
            <div>
                Enter your <strong>Anthropic Claude API key</strong> above to generate
                personalized interview questions.
                Get one at <strong>console.anthropic.com</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        run = st.button("🤖  Generate Questions", use_container_width=True)

    if run:
        with st.spinner("Claude AI is crafting personalized questions…"):
            result = generate_interview_questions(
                candidate_name=candidate,
                resume_text=resume["text"],
                job_description=jd,
                missing_skills=missing,
                api_key=api_key,
            )

        if result["error"]:
            st.error(f"❌ Error: {result['error']}")
        elif result["questions"]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="skill-section-label" style="color:#818cf8;">GENERATED INTERVIEW QUESTIONS</div>', unsafe_allow_html=True)

            # JS copy-to-clipboard
            all_qs = "\n".join([f"Q{i}. {q}" for i, q in enumerate(result["questions"], 1)])
            copy_js = f"""
            <script>
            function copyAllQs() {{
                const text = {repr(all_qs)};
                navigator.clipboard.writeText(text).then(() => {{
                    const btn = document.getElementById('copyAllBtn');
                    btn.innerText = '✓ Copied!';
                    btn.style.color = '#34d399';
                    setTimeout(() => {{ btn.innerText = '📋 Copy All'; btn.style.color = '#818cf8'; }}, 2000);
                }});
            }}
            </script>
            <div style="display:flex;justify-content:flex-end;margin-bottom:0.5rem;">
                <span id="copyAllBtn"
                      onclick="copyAllQs()"
                      style="font-size:0.75rem;color:#818cf8;cursor:pointer;font-family:'Inter',sans-serif;
                             font-weight:600;padding:4px 10px;border:1px solid rgba(99,102,241,0.3);
                             border-radius:6px;transition:all 0.2s;">
                    📋 Copy All
                </span>
            </div>
            """
            st.markdown(copy_js, unsafe_allow_html=True)

            for i, q in enumerate(result["questions"], 1):
                anim_delay  = f"animation-delay:{(i-1)*0.08}s;"
                q_js_safe   = q.replace("'", "\u2019")  # replace single quote for JS safety
                st.markdown(f"""
                <div class="q-item" style="{anim_delay}" onclick="navigator.clipboard.writeText('{q_js_safe}')">
                    <div class="q-num">Q{i}</div>
                    <div class="q-text">
                        {q}
                        <div class="q-copy-hint">Click to copy</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No questions generated. Please try again.")
