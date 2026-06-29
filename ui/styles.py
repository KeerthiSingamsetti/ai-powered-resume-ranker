"""ui/styles.py — Sky Blue Background + Gold Accents Theme (refined, professional)."""

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════════════════════
   BASE RESET & TYPOGRAPHY
══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}
h1, h2, h3, h4, h5, h6, .hero-title, .pg-heading {
    font-family: 'Outfit', -apple-system, sans-serif !important;
}

/* ══════════════════════════════════════════════════════
   BACKGROUND — CSS gradient mesh (no external image needed,
   no licensing risk, matches palette, loads instantly)
══════════════════════════════════════════════════════ */
.stApp {
    background:
        radial-gradient(at 15% 15%, rgba(14,165,233,0.28) 0px, transparent 45%),
        radial-gradient(at 85% 0%, rgba(240,180,41,0.22) 0px, transparent 45%),
        radial-gradient(at 0% 85%, rgba(56,189,248,0.24) 0px, transparent 45%),
        radial-gradient(at 90% 90%, rgba(201,134,10,0.18) 0px, transparent 45%),
        linear-gradient(135deg, #eaf6ff 0%, #dbeefe 50%, #eef9ff 100%) !important;
    background-size: 100% 100%;
    background-attachment: fixed;
    min-height: 100vh;
    overflow-x: hidden;
}
/* Soft dot-grid texture — visible but light, gives the page a "designed" feel */
.stApp {
    background-image:
        radial-gradient(at 15% 15%, rgba(14,165,233,0.28) 0px, transparent 45%),
        radial-gradient(at 85% 0%, rgba(240,180,41,0.22) 0px, transparent 45%),
        radial-gradient(at 0% 85%, rgba(56,189,248,0.24) 0px, transparent 45%),
        radial-gradient(at 90% 90%, rgba(201,134,10,0.18) 0px, transparent 45%),
        radial-gradient(circle, rgba(12,74,110,0.10) 1px, transparent 1px),
        linear-gradient(135deg, #eaf6ff 0%, #dbeefe 50%, #eef9ff 100%) !important;
    background-size: auto, auto, auto, auto, 22px 22px, 100% 100%;
}
/* Larger, clearly-moving ambient blobs */
.stApp::before {
    content: '';
    position: fixed;
    top: -20%; left: -12%;
    width: 60vw; height: 60vw;
    background: radial-gradient(circle, rgba(240,180,41,0.20) 0%, transparent 70%);
    border-radius: 50%;
    animation: orbFloat1 20s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -15%; right: -10%;
    width: 50vw; height: 50vw;
    background: radial-gradient(circle, rgba(14,165,233,0.22) 0%, transparent 70%);
    border-radius: 50%;
    animation: orbFloat2 24s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes orbFloat1 {
    0%, 100% { transform: translate(0,0) scale(1); }
    50%      { transform: translate(6%,6%) scale(1.08); }
}
@keyframes orbFloat2 {
    0%, 100% { transform: translate(0,0) scale(1); }
    50%      { transform: translate(-6%,-6%) scale(1.08); }
}

/* ══════════════════════════════════════════════════════
   TOP STRIPE — Static gold (no shimmer; cleaner, calmer)
══════════════════════════════════════════════════════ */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c9860a 0%, #f0b429 50%, #c9860a 100%);
    z-index: 9999;
}

/* ══════════════════════════════════════════════════════
   STREAMLIT CHROME CLEANUP
══════════════════════════════════════════════════════ */
#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container {
    padding: 3rem 3.5rem 5rem !important;
    max-width: 1300px !important;
    position: relative;
    z-index: 1;
}

/* ══════════════════════════════════════════════════════
   ANIMATIONS (kept subtle, used sparingly)
══════════════════════════════════════════════════════ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.96); }
    to   { opacity: 1; transform: scale(1); }
}

/* ══════════════════════════════════════════════════════
   HERO SECTION
══════════════════════════════════════════════════════ */
.hero-wrap {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    animation: fadeInUp 0.6s ease both;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #c9860a;
    border: 1px solid rgba(240,180,41,0.4);
    border-radius: 99px;
    padding: 0.4rem 1.3rem;
    margin-bottom: 1.6rem;
    background: rgba(240,180,41,0.10);
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase;
}
.hero-eyebrow-dot {
    width: 6px; height: 6px;
    background: #f0b429;
    border-radius: 50%;
}
.hero-title {
    font-size: clamp(3rem, 6vw, 5rem) !important;
    font-weight: 900 !important;
    letter-spacing: -0.04em !important;
    line-height: 1.08 !important;
    margin: 0 0 0.5rem !important;
    background: linear-gradient(135deg, #0c4a6e 0%, #0369a1 35%, #0ea5e9 65%, #38bdf8 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
.hero-title-accent {
    display: block;
    background: linear-gradient(135deg, #c9860a 0%, #f0b429 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    color: #0c4a6e !important;
    font-size: 1.1rem !important;
    line-height: 1.7 !important;
    margin: 0 auto 2rem !important;
    max-width: 640px;
    font-family: 'Inter', sans-serif !important;
}
.hero-stats-row {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}
.hero-stat { text-align: center; }
.hero-stat-num {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #c9860a;
    line-height: 1;
}
.hero-stat-label {
    font-size: 0.72rem;
    color: #0369a1;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* ══════════════════════════════════════════════════════
   HOW IT WORKS — 3 STEPS
══════════════════════════════════════════════════════ */
.steps-wrap {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.2rem;
    margin: 1.5rem 0 2rem;
    animation: fadeInUp 0.6s ease both;
}
.step-card {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}
.step-card:hover {
    border-color: rgba(240,180,41,0.45);
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(15,23,42,0.06);
}
.step-icon-wrap {
    width: 44px; height: 44px;
    background: rgba(240,180,41,0.12);
    border: 1px solid rgba(240,180,41,0.3);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
}
.step-num {
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: #c9860a;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
    font-family: 'Inter', sans-serif;
}
.step-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #0c4a6e;
    font-family: 'Outfit', sans-serif;
}
.step-desc {
    font-size: 0.78rem;
    color: #0369a1;
    line-height: 1.5;
    margin-top: 0.2rem;
    font-family: 'Inter', sans-serif;
}

/* ══════════════════════════════════════════════════════
   SECTION LABELS
══════════════════════════════════════════════════════ */
.section-label {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    color: #475569;
    margin-top: 2rem;
    margin-bottom: 1rem;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif !important;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(15,23,42,0.1);
}

/* ══════════════════════════════════════════════════════
   GLASS CARDS — neutral borders, gold only on hover (accent, not noise)
══════════════════════════════════════════════════════ */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.78) !important;
    border: 1px solid rgba(15,23,42,0.08) !important;
    border-radius: 18px !important;
    padding: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(240,180,41,0.4) !important;
    box-shadow: 0 8px 28px rgba(15,23,42,0.07) !important;
}
.input-card-title {
    font-size: 0.9rem;
    font-weight: 700;
    color: #0c4a6e;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Outfit', sans-serif;
}
.badge-pill {
    font-size: 0.6rem;
    font-weight: 700;
    background: rgba(240,180,41,0.12);
    color: #c9860a;
    border: 1px solid rgba(240,180,41,0.35);
    border-radius: 99px;
    padding: 2px 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}
.file-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(15,23,42,0.04);
    border: 1px solid rgba(15,23,42,0.1);
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 0.78rem;
    color: #475569;
    margin: 4px 4px 0 0;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}
.jd-meta {
    font-size: 0.78rem;
    color: #c9860a;
    margin-top: 0.75rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}

/* ══════════════════════════════════════════════════════
   STATS SUMMARY BANNER
══════════════════════════════════════════════════════ */
.stats-banner {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
    animation: fadeInUp 0.5s ease both;
}
.stat-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    transition: border-color 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}
.stat-card.green::after  { background: #10b981; }
.stat-card.blue::after   { background: #0ea5e9; }
.stat-card.amber::after  { background: #f0b429; }
.stat-card.purple::after { background: #c9860a; }
.stat-card.red::after    { background: #ef4444; }
.stat-card:hover { border-color: rgba(15,23,42,0.16); transform: translateY(-2px); }
.stat-card-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #0369a1;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
}
.stat-card-value {
    font-size: 2rem;
    font-weight: 800;
    color: #0c4a6e;
    line-height: 1;
    font-family: 'Outfit', sans-serif;
}
.stat-card-sub {
    font-size: 0.72rem;
    color: #0369a1;
    margin-top: 0.3rem;
    font-family: 'Inter', sans-serif;
}

/* ══════════════════════════════════════════════════════
   TABS — GOLD SELECTED (your one strong accent use — kept as-is, it works)
══════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.82) !important;
    border: 1px solid rgba(15,23,42,0.08) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    color: #0369a1 !important;
    transition: all 0.2s !important;
    background: transparent !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #c9860a !important;
    background: rgba(240,180,41,0.07) !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #c9860a 0%, #f0b429 100%) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 12px rgba(240,180,41,0.35) !important;
    border-radius: 10px !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 2rem 0 0 !important;
}

/* ══════════════════════════════════════════════════════
   EMPTY STATES
══════════════════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    background: rgba(255,255,255,0.6);
    border: 1px dashed rgba(15,23,42,0.15);
    border-radius: 18px;
    animation: fadeIn 0.4s ease;
}
.empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state-title {
    font-size: 1.05rem; font-weight: 700; color: #0c4a6e;
    margin-bottom: 0.5rem;
    font-family: 'Outfit', sans-serif;
}
.empty-state-desc { font-size: 0.85rem; color: #0369a1; line-height: 1.6; font-family: 'Inter', sans-serif; }

/* ══════════════════════════════════════════════════════
   PAGE HEADINGS
══════════════════════════════════════════════════════ */
.pg-heading {
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    color: #0c4a6e !important;
    margin: 0 0 0.35rem !important;
    letter-spacing: -0.025em !important;
    font-family: 'Outfit', sans-serif !important;
    animation: fadeInUp 0.45s ease both;
}
.pg-sub {
    font-size: 0.85rem !important;
    color: #0369a1 !important;
    margin-bottom: 2rem !important;
    font-family: 'Inter', sans-serif !important;
}

/* ══════════════════════════════════════════════════════
   CUSTOM METRIC CARDS
══════════════════════════════════════════════════════ */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.m-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
    transition: border-color 0.2s, transform 0.2s;
}
.m-card:hover { border-color: rgba(15,23,42,0.16); transform: translateY(-2px); }
.m-card-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #0369a1;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    font-family: 'Inter', sans-serif;
}
.m-card-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #c9860a;
    line-height: 1;
    font-family: 'Outfit', sans-serif;
}
.m-card-value.green  { color: #059669; }
.m-card-value.amber  { color: #c9860a; }
.m-card-value.red    { color: #dc2626; }
.m-card-value.purple { color: #7c3aed; }
.m-card-sub {
    font-size: 0.7rem;
    color: #0369a1;
    margin-top: 0.3rem;
    font-family: 'Inter', sans-serif;
}

/* ══════════════════════════════════════════════════════
   RANKING LEADERBOARD
══════════════════════════════════════════════════════ */
.rank-row {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
}
.rank-row:hover {
    border-color: rgba(240,180,41,0.4);
    transform: translateX(4px);
    box-shadow: -3px 0 16px rgba(15,23,42,0.06);
}
.rank-row.gold   { border-left: 3px solid #f0b429; }
.rank-row.silver { border-left: 3px solid #64748b; }
.rank-row.bronze { border-left: 3px solid #b45309; }
.rank-pos {
    font-size: 1.6rem;
    font-weight: 800;
    min-width: 2.8rem;
    text-align: center;
    font-family: 'Outfit', sans-serif;
}
.rank-info { flex: 1; }
.rank-name {
    font-size: 1rem;
    font-weight: 700;
    color: #0c4a6e;
    margin-bottom: 0.1rem;
    font-family: 'Outfit', sans-serif;
}
.rank-tag {
    font-size: 0.68rem;
    color: #0369a1;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}
.rank-bar-bg {
    background: rgba(15,23,42,0.06);
    border-radius: 99px;
    height: 5px;
    margin-top: 10px;
    overflow: hidden;
}
.rank-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 1s ease;
}
.rank-pct {
    font-size: 1.55rem;
    font-weight: 900;
    min-width: 5.5rem;
    text-align: right;
    font-family: 'Outfit', sans-serif;
    letter-spacing: -0.03em;
}

/* ══════════════════════════════════════════════════════
   SKILL GAP BADGES
══════════════════════════════════════════════════════ */
.skill-section-label {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    font-family: 'Inter', sans-serif;
}
.skill-wrap { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 1.2rem; }
.stag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 5px 13px;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: transform 0.15s;
    cursor: default;
}
.stag:hover { transform: translateY(-1px); }
.stag-match {
    background: rgba(5,150,105,0.1);
    color: #059669;
    border: 1px solid rgba(5,150,105,0.3);
}
.stag-missing {
    background: rgba(220,38,38,0.1);
    color: #dc2626;
    border: 1px solid rgba(220,38,38,0.25);
}
.stag-extra {
    background: rgba(240,180,41,0.12);
    color: #c9860a;
    border: 1px solid rgba(240,180,41,0.3);
}

/* ══════════════════════════════════════════════════════
   DONUT MATCH INDICATOR
══════════════════════════════════════════════════════ */
.donut-wrap {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.donut-info { flex: 1; }
.donut-pct {
    font-size: 2.2rem;
    font-weight: 900;
    font-family: 'Outfit', sans-serif;
    line-height: 1;
    letter-spacing: -0.03em;
    color: #c9860a;
}
.donut-label {
    font-size: 0.75rem;
    color: #0369a1;
    margin-top: 0.2rem;
    font-family: 'Inter', sans-serif;
}
.match-bar-outer {
    width: 100%;
    height: 8px;
    background: rgba(15,23,42,0.06);
    border-radius: 99px;
    overflow: hidden;
    margin-top: 0.75rem;
}
.match-bar-inner {
    height: 100%;
    border-radius: 99px;
    transition: width 1s ease;
}

/* ══════════════════════════════════════════════════════
   TRUST SCORE
══════════════════════════════════════════════════════ */
.trust-panel {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: scaleIn 0.45s ease both;
    text-align: center;
}
.trust-score-label {
    font-size: 0.72rem;
    color: #0369a1;
    font-family: 'Inter', sans-serif;
    margin-top: 0.15rem;
}
.trust-verdict {
    font-size: 1rem;
    font-weight: 700;
    margin-top: 0.8rem;
    font-family: 'Outfit', sans-serif;
}
.flag-row {
    background: rgba(220,38,38,0.06);
    border-left: 3px solid #dc2626;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 0;
    color: #991b1b;
    font-size: 0.86rem;
    line-height: 1.55;
    font-family: 'Inter', sans-serif;
}
.ok-row {
    background: rgba(5,150,105,0.06);
    border-left: 3px solid #059669;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 0;
    color: #065f46;
    font-size: 0.86rem;
    line-height: 1.55;
    font-family: 'Inter', sans-serif;
}

/* ══════════════════════════════════════════════════════
   BIAS DETECTOR CARDS
══════════════════════════════════════════════════════ */
.bias-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.9rem;
    transition: all 0.2s;
}
.bias-card.sev-high  { border-left: 3px solid #dc2626; }
.bias-card.sev-med   { border-left: 3px solid #f0b429; }
.bias-card.sev-low   { border-left: 3px solid #0369a1; }
.bias-card:hover { transform: translateX(3px); }
.sev-HIGH {
    background: rgba(220,38,38,0.1); color: #991b1b;
    border: 1px solid rgba(220,38,38,0.3);
    padding: 3px 10px; border-radius: 6px;
    font-size: 0.68rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}
.sev-MEDIUM {
    background: rgba(240,180,41,0.12); color: #c9860a;
    border: 1px solid rgba(240,180,41,0.4);
    padding: 3px 10px; border-radius: 6px;
    font-size: 0.68rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}
.sev-LOW {
    background: rgba(3,105,161,0.1); color: #0369a1;
    border: 1px solid rgba(3,105,161,0.25);
    padding: 3px 10px; border-radius: 6px;
    font-size: 0.68rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}

/* ══════════════════════════════════════════════════════
   INTERVIEW QUESTION CARDS
══════════════════════════════════════════════════════ */
.q-item {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 14px;
    padding: 1.15rem 1.4rem;
    margin: 0.7rem 0;
    color: #0c4a6e;
    font-size: 0.93rem;
    line-height: 1.65;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    transition: all 0.2s;
    cursor: pointer;
}
.q-item:hover {
    border-color: rgba(240,180,41,0.4);
    transform: translateX(3px);
    box-shadow: -3px 0 14px rgba(15,23,42,0.06);
}
.q-num {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    background: linear-gradient(135deg, #c9860a, #f0b429);
    border-radius: 8px;
    color: #fff;
    font-weight: 800;
    font-size: 0.78rem;
    flex-shrink: 0;
    font-family: 'Outfit', sans-serif;
    margin-top: 2px;
}
.q-text { flex: 1; font-family: 'Inter', sans-serif; color: #0c4a6e; }
.q-copy-hint {
    font-size: 0.7rem;
    color: #0369a1;
    font-family: 'Inter', sans-serif;
    margin-top: 0.3rem;
}

/* ══════════════════════════════════════════════════════
   CANDIDATE COMPARISON TABLE
══════════════════════════════════════════════════════ */
.comp-table-wrap {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(15,23,42,0.08);
    border-radius: 18px;
    overflow: hidden;
}
.comp-table-head {
    display: grid;
    background: rgba(15,23,42,0.03);
    border-bottom: 1px solid rgba(15,23,42,0.08);
    padding: 0.9rem 1.4rem;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #475569;
    text-transform: uppercase;
    font-family: 'Inter', sans-serif;
}
.comp-table-row {
    display: grid;
    padding: 1rem 1.4rem;
    border-bottom: 1px solid rgba(15,23,42,0.05);
    align-items: center;
    transition: background 0.15s;
}
.comp-table-row:last-child { border-bottom: none; }
.comp-table-row:hover { background: rgba(15,23,42,0.02); }
.comp-name {
    font-size: 0.9rem;
    font-weight: 700;
    color: #0c4a6e;
    font-family: 'Outfit', sans-serif;
}
.comp-cell {
    font-size: 0.88rem;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
    text-align: center;
    color: #0c4a6e;
}

/* ══════════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #c9860a 0%, #f0b429 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    padding: 0.7rem 1.8rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 12px rgba(240,180,41,0.28) !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    opacity: 0.92 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(240,180,41,0.4) !important;
}
.stButton > button:active { transform: translateY(1px) !important; }
.stDownloadButton > button {
    background: rgba(3,105,161,0.08) !important;
    color: #0369a1 !important;
    border: 1px solid rgba(3,105,161,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(3,105,161,0.16) !important;
    border-color: rgba(3,105,161,0.5) !important;
}

/* ══════════════════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    border: 1.5px dashed rgba(15,23,42,0.15) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.4) !important;
    transition: all 0.25s !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(240,180,41,0.45) !important;
    background: rgba(240,180,41,0.04) !important;
}
[data-testid="stFileUploader"] section { background: transparent !important; }

/* ══════════════════════════════════════════════════════
   FORM ELEMENTS
══════════════════════════════════════════════════════ */
textarea, input[type="text"], input[type="password"] {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(15,23,42,0.12) !important;
    border-radius: 10px !important;
    color: #0c4a6e !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
}
textarea:focus, input:focus {
    border-color: rgba(240,180,41,0.55) !important;
    box-shadow: 0 0 0 3px rgba(240,180,41,0.1) !important;
    outline: none !important;
}
textarea::placeholder, input::placeholder { color: #94a3b8 !important; }
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(15,23,42,0.12) !important;
    border-radius: 10px !important;
    color: #0c4a6e !important;
    font-family: 'Inter', sans-serif !important;
}

/* ══════════════════════════════════════════════════════
   NATIVE METRIC OVERRIDES
══════════════════════════════════════════════════════ */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(15,23,42,0.08) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.3rem !important;
}
[data-testid="metric-container"] label {
    color: #0369a1 !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMetricValue"] {
    color: #c9860a !important;
    font-weight: 800 !important;
    font-size: 1.65rem !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ══════════════════════════════════════════════════════
   DIVIDER & SCROLLBAR
══════════════════════════════════════════════════════ */
hr { border-color: rgba(15,23,42,0.1) !important; margin: 1.5rem 0 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(240,180,41,0.3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(240,180,41,0.5); }
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSpinner"] > div {
    color: #c9860a !important;
    font-family: 'Inter', sans-serif !important;
}
</style>
"""