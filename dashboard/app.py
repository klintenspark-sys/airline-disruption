import streamlit as st
 
st.set_page_config(
    page_title="AirOps AI",
    page_icon="✈",
    layout="wide"
)
 
st.markdown("""
<style>
html, body, [class*="css"] { font-family: Arial, 'Segoe UI', sans-serif; }
.stApp { background:#f5f7fb; color:#172033; }
#MainMenu, footer, header { visibility:hidden; }
[data-testid='stSidebar'], [data-testid='collapsedControl'] { display:none !important; }
.block-container { max-width:1120px; padding-top:1.2rem; padding-bottom:1rem; }

.hero { text-align:center; padding:12px 12px 20px; }
.hero h1 { font-size:3rem; font-weight:800; color:#111827; margin:8px 0; letter-spacing:-1px; }
.hero p { color:#52627a; font-size:1.12rem; max-width:700px; margin:0 auto; line-height:1.45; }
.badge { background:#1e3a5f; color:#ffffff; font-size:.82rem; padding:7px 16px; border-radius:20px; font-weight:700; letter-spacing:.7px; display:inline-block; margin-bottom:5px; }

.role-card {
    background:#ffffff; border:1px solid #cbd5e1; border-radius:14px;
    padding:22px 26px 18px; text-align:center; min-height:330px;
    box-shadow:0 5px 18px rgba(15,23,42,.06);
}
.role-card:hover { border-color:#7c2d12; box-shadow:0 9px 24px rgba(15,23,42,.10); }
.role-icon { font-size:2.6rem; margin-bottom:6px; }
.role-title { color:#111827; font-size:1.45rem; font-weight:800; margin-bottom:6px; }
.role-desc { color:#52627a; font-size:.98rem; line-height:1.4; margin:0 auto 10px; max-width:380px; }
.role-features { text-align:left; list-style:none; padding:0; margin:8px auto 4px; max-width:330px; }
.role-features li { color:#475569; font-size:.92rem; padding:3px 0; }
.role-features li::before { content:"✓ "; color:#059669; font-weight:800; }

.stButton > button { min-height:48px; font-size:1rem; font-weight:700; border-radius:10px; }
.divider { border:none; border-top:1px solid #dbe3ef; margin:18px 0 10px; }
.tech-row { display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin-top:8px; }
.tech-pill { background:#fff; border:1px solid #d7e0ec; color:#52627a; font-size:.78rem; padding:4px 10px; border-radius:20px; }

@media (max-width: 800px) {
  .hero h1 { font-size:2.4rem; }
  .role-card { min-height:auto; padding:18px; }
}

/* V24 equal-height cards */
.role-card{min-height:420px!important;height:420px!important;box-sizing:border-box!important;display:flex!important;flex-direction:column!important}.role-features{margin-top:auto!important;margin-bottom:0!important}
</style>
""", unsafe_allow_html=True)
 
st.markdown("""
<div class="hero">
<span class="badge">AI-POWERED AIRLINE OPERATIONS</span>
<h1>✈ AirOps AI</h1>
<p>Airline Disruption Prediction & Recovery powered by 5 coordinated AI agents</p>
</div>
""", unsafe_allow_html=True)
 
col1, col2 = st.columns([1, 1], gap="medium")
 
with col1:
    st.markdown("""
<div class="role-card">
<div class="role-icon">🖥</div>
<div class="role-title">Operations Team</div>
<div class="role-desc">Full disruption control center for airline operations staff</div>
<ul class="role-features">
<li>Live weather & flight board</li>
<li>AI multi-agent analysis</li>
<li>Recovery plan generation</li>
<li>Evaluator scoring & approval</li>
<li>Execution log & staff metrics</li>
</ul>
</div>
    """, unsafe_allow_html=True)
    if st.button("Enter as Ops Team →", type="primary", use_container_width=True):
        st.switch_page("pages/1_Ops_Team.py")
 
with col2:
    st.markdown("""
<div class="role-card">
<div class="role-icon">👤</div>
<div class="role-title">Passenger</div>
<div class="role-desc">Personal disruption status and rebooking details for travellers</div>
<ul class="role-features">
<li>Check your flight status</li>
<li>View new seat assignment</li>
<li>New gate & boarding time</li>
<li>Meal voucher eligibility</li>
<li>SMS & email confirmation</li>
</ul>
</div>
    """, unsafe_allow_html=True)
    if st.button("Enter as Passenger →", type="primary", use_container_width=True):
        st.switch_page("pages/2_Passenger.py")
 
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;">
<div style="color:#52627a;font-size:0.78rem;margin-bottom:10px;">Powered by</div>
<div class="tech-row">
<span class="tech-pill">Neuro SAN Studio</span>
<span class="tech-pill">Ollama LLM</span>
<span class="tech-pill">FastAPI</span>
<span class="tech-pill">Streamlit</span>
<span class="tech-pill">llama3.1:8b</span>
</div>
</div>
""", unsafe_allow_html=True)


