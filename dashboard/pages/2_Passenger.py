import streamlit as st
import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tools.operational_state import get_operational_state
import json

st.set_page_config(page_title="My Flight — AirOps AI",page_icon="👤",layout="centered",initial_sidebar_state="collapsed")
dark=False  # fixed readable light theme
t={"bg":"#111827" if dark else "#f3f4f6","surface":"#1f2937" if dark else "#fff","text":"#f9fafb" if dark else "#172033","muted":"#d1d5db" if dark else "#475569","border":"#4b5563" if dark else "#cbd5e1"}
css = """<style>
html,body,[class*=\"css\"]{font-family:Arial,\"Segoe UI\",sans-serif!important;font-size:17px!important}.stApp{background:BG!important;color:TEXT!important}#MainMenu,footer,header{visibility:hidden}
.card{background:SURFACE;border:1px solid BORDER;border-radius:14px;padding:20px;margin:12px 0}.title{font-size:2rem;font-weight:800;color:TEXT}.muted{color:MUTED}.route{font-size:2rem;font-weight:800;color:TEXT;display:flex;justify-content:space-between}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px}.item{background:ITEMBG;padding:12px;border-radius:8px}.label{font-size:.78rem;color:MUTED;text-transform:uppercase}.value{font-size:1.05rem;font-weight:700;color:TEXT}.banner{padding:14px 16px;border-radius:10px;font-weight:800;margin:12px 0}.on{background:ONBG;color:ONTEXT;border:1px solid #22c55e}.delay{background:DELAYBG;color:DELAYTEXT;border:1px solid #f59e0b}.cancel{background:CANCELBG;color:CANCELTEXT;border:1px solid #ef4444}
[data-testid="stAppViewContainer"] p,[data-testid="stAppViewContainer"] label,[data-testid="stAppViewContainer"] h1,[data-testid="stAppViewContainer"] h2,[data-testid="stAppViewContainer"] h3{color:TEXT!important}
[data-testid="stTextInput"] input{background:SURFACE!important;color:TEXT!important;border-color:BORDER!important}
[data-testid="stAlert"]{color:TEXT!important;border:1px solid BORDER!important}
</style>"""
css = (css.replace("BG", t["bg"])
    .replace("SURFACE", t["surface"])
    .replace("TEXT", t["text"])
    .replace("MUTED", t["muted"])
    .replace("BORDER", t["border"])
    .replace("ITEMBG", "#26313f" if dark else "#f8fafc")
    .replace("ONBG", "#123524" if dark else "#dcfce7")
    .replace("ONTEXT", "#bbf7d0" if dark else "#166534")
    .replace("DELAYBG", "#3f3215" if dark else "#fffbeb")
    .replace("DELAYTEXT", "#fde68a" if dark else "#92400e")
    .replace("CANCELBG", "#451a1a" if dark else "#fff1f2")
    .replace("CANCELTEXT", "#fecaca" if dark else "#991b1b"))
st.markdown(css, unsafe_allow_html=True)

st.markdown('<div class="card"><div class="title">👤 Passenger Status</div><div class="muted">Search your booking using your 6-character PNR.</div></div>',unsafe_allow_html=True)
if st.button("← Back to Home"): st.switch_page("app.py")
DATA_DIR=os.path.join(os.path.dirname(__file__),"..","..","mock_data")
def load_json(name,default):
    try:
        with open(os.path.join(DATA_DIR,name),"r",encoding="utf-8") as f:return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):return default
passengers=load_json("passengers.json",[]); recovery_state=load_json("recovery_state.json",{})
if "pax_pnr" not in st.session_state:
    st.session_state.pax_pnr=""
if "pnr_input" not in st.session_state:
    st.session_state.pnr_input=""

st.markdown("### Find Your Booking")

with st.form("pnr_search",clear_on_submit=False):
    a,b=st.columns([4,1])
    with a:
        st.text_input(
            "PNR Number",
            max_chars=6,
            placeholder="Enter 6-character PNR",
            key="pnr_input"
        )
    with b:
        st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
        go=st.form_submit_button("🔎 Search",type="primary",use_container_width=True)

if go:
    entered_pnr=st.session_state.pnr_input.strip().upper()
    st.session_state.pax_pnr=entered_pnr
    st.session_state["pnr_was_reset"]=False

def reset_pnr_search():
    # Clear the active search and every page-local result/recovery display state.
    # The persisted operational recovery record is intentionally not deleted;
    # it will only be shown again after a new PNR search.
    st.session_state.pax_pnr=""
    st.session_state.pnr_input=""
    st.session_state["pnr_was_reset"]=True
    for key in [
        "passenger_result",
        "selected_passenger",
        "passenger_status",
        "passenger_recovery",
        "recovery",
        "recovery_booking",
        "confirmed_recovery"
    ]:
        st.session_state.pop(key,None)

if st.session_state.pax_pnr:
    reset_col, reset_space = st.columns([1.2,5])
    with reset_col:
        st.button(
            "↻ Reset PNR",
            use_container_width=True,
            key="reset_pnr",
            on_click=reset_pnr_search
        )

pnr=st.session_state.pax_pnr
if not pnr:
    st.info("Enter your PNR and click Search.")
else:
    passenger=next((x for x in passengers if x.get("pnr","").upper()==pnr),None)
    if not passenger:st.error("Booking not found. Check the PNR and search again.")
    else:
        s=get_operational_state(passenger["flight_id"]); status=s["effective_status"]; recovery=recovery_state.get(pnr)
        if status=="On Time":st.markdown('<div class="banner on">✅ Your flight is ON TIME — no active exceptions and no recovery action is required. Have a pleasant journey.</div>',unsafe_allow_html=True)
        elif status=="Delayed":st.markdown(f'<div class="banner delay">⚠️ Your flight is DELAYED by {s["current_delay_minutes"]} minutes due to {s["cause"]}.</div>',unsafe_allow_html=True)
        else:st.markdown(f'<div class="banner cancel">🚫 Your flight is CANCELLED due to {s["cause"]}.</div>',unsafe_allow_html=True)
        st.markdown(f"""<div class="card"><div style="display:flex;justify-content:space-between"><div><div class="title">{s['flight_id']}</div><div class="muted">American Airlines · {s['aircraft']}</div></div><div><div class="label">PNR</div><div class="value">{pnr}</div></div></div><div class="route"><span>{s['origin']}</span><span>✈</span><span>{s['destination']}</span></div><div class="grid"><div class="item"><div class="label">Passenger</div><div class="value">{passenger['passenger_name']}</div></div><div class="item"><div class="label">Status</div><div class="value">{status}</div></div><div class="item"><div class="label">Original Seat</div><div class="value">{passenger['seat']}</div></div><div class="item"><div class="label">Original Gate</div><div class="value">{passenger['gate']}</div></div><div class="item"><div class="label">Scheduled Departure</div><div class="value">{s['scheduled_departure'][11:16]}</div></div><div class="item"><div class="label">Scheduled Arrival</div><div class="value">{s.get('scheduled_arrival','')[11:16]}</div></div><div class="item"><div class="label">Operational Stage</div><div class="value">{s.get('operational_stage','At Gate')}</div></div><div class="item"><div class="label">Current Location</div><div class="value">{s.get('current_location',s['origin'])}</div></div></div></div>""",unsafe_allow_html=True)
        if status in ("Delayed","Cancelled"):
            if recovery:
                dep=recovery.get("new_departure","Pending").replace("T"," ")
                st.markdown(f"""<div class="card"><h3>✈ Confirmed Recovery Booking</h3><div class="grid"><div class="item"><div class="label">New Flight</div><div class="value">{recovery.get('new_flight','Pending')}</div></div><div class="item"><div class="label">New Departure</div><div class="value">{dep}</div></div><div class="item"><div class="label">New Gate</div><div class="value">{recovery.get('new_gate','Pending')}</div></div><div class="item"><div class="label">New Seat</div><div class="value">{recovery.get('seat','Pending')}</div></div></div></div>""",unsafe_allow_html=True)
                if recovery.get("voucher_code"):st.success(f"🍽 Meal voucher: {recovery['voucher_code']}")
                st.success("📧 Email, 📱 SMS and 🔔 app notifications are synchronized with this recovery record.")
            else:st.info("A disruption is active, but no recovery booking has been applied yet. The Ops Team must apply the Recovery Plan first.")
        else:
            st.markdown(f"""<div class="card"><h3>Boarding Information</h3><div class="grid"><div class="item"><div class="label">Gate</div><div class="value">{passenger['gate']}</div></div><div class="item"><div class="label">Seat</div><div class="value">{passenger['seat']}</div></div><div class="item"><div class="label">Terminal</div><div class="value">Terminal {passenger['terminal']}</div></div><div class="item"><div class="label">Cabin</div><div class="value">{passenger['cabin']}</div></div></div></div>""",unsafe_allow_html=True)
st.markdown("""<style>div[data-testid="stForm"]{background:#fff;border:1px solid #cbd5e1;border-radius:12px;padding:14px 16px 8px}div[data-testid="stTextInput"] input{min-height:48px!important;font-size:1.08rem!important;font-weight:700;letter-spacing:1px}div[data-testid="stFormSubmitButton"] button{min-height:48px!important;font-weight:700!important;background:#7c2d12!important;border-color:#7c2d12!important}</style>""",unsafe_allow_html=True)
