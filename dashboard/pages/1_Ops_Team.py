import streamlit as st
import httpx
import sys
import os
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tools.operational_state import get_all_operational_states, get_operational_state

st.set_page_config(page_title="Ops Team — AirOps AI", page_icon="🖥", layout="wide", initial_sidebar_state="collapsed")

dark = False  # fixed readable light theme
t = {"bg":"#111827" if dark else "#f3f4f6", "surface":"#1f2937" if dark else "#ffffff", "text":"#f9fafb" if dark else "#172033", "muted":"#d1d5db" if dark else "#475569", "border":"#4b5563" if dark else "#cbd5e1"}
st.markdown(f"""
<style>
html, body, [class*="css"] {{ font-family: Arial, 'Segoe UI', sans-serif !important; font-size:18px !important; }}
.stApp {{ background:{t['bg']} !important; color:{t['text']} !important; }}
#MainMenu, footer, header {{ visibility:hidden; }} .block-container {{ padding-top:1rem !important; }}
.header {{ background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; padding:20px 24px; margin-bottom:18px; }}
.header h1 {{ margin:0; color:{t['text']}; font-size:2rem; }} .header p {{ color:{t['muted']}; margin:5px 0 0; }}
.metric {{ background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:18px; }}
.metric .v {{ font-size:2rem; font-weight:800; color:{t['text']}; }} .metric .l {{ color:{t['muted']}; font-size:.9rem; }}
.section {{ font-size:1rem; font-weight:800; text-transform:uppercase; letter-spacing:.7px; color:{t['muted']}; margin:18px 0 10px; }}
.weather {{ display:flex; justify-content:space-between; align-items:center; padding:9px 14px; min-height:58px; border-radius:9px; margin:6px 0; color:{t['text']}; }}
.high {{ background:{'#4a2024' if dark else '#fff1f2'}; border:1px solid #dc2626; border-left:6px solid #dc2626; }}
.medium {{ background:{'#493916' if dark else '#fffbeb'}; border:1px solid #b45309; border-left:6px solid #b45309; }}
.low {{ background:{'#153b2b' if dark else '#ecfdf5'}; border:1px solid #047857; border-left:6px solid #047857; }}
.ap {{ font-size:1rem; font-weight:800; }} .wd {{ color:{t['muted']}; font-size:.82rem; }}
.badge {{ min-width:82px; min-height:34px; display:inline-flex; align-items:center; justify-content:center; border-radius:9px; font-size:.88rem; font-weight:800; color:white; padding:5px 12px; }}
.b-high,.b-cancelled {{ background:#dc2626; }} .b-medium,.b-delayed {{ background:#d97706; }} .b-low,.b-ontime {{ background:#059669; }}
.flight {{ display:grid; grid-template-columns:90px 120px 1fr 120px; gap:12px; align-items:center; background:{t['surface']}; border:1px solid {t['border']}; border-radius:10px; padding:10px 14px; margin:7px 0; }}
.fid {{ font-weight:800; color:#9a3412; }} .route {{ font-weight:700; color:{t['text']}; }} .info {{ color:{t['muted']}; font-size:.88rem; }}
.impact {{ background:{t['surface']}; border:1px solid {t['border']}; border-radius:10px; padding:14px; text-align:center; }} .impact strong {{ font-size:1.4rem; color:{t['text']}; display:block; }} .impact span {{ color:{t['muted']}; font-size:.8rem; }}


/* Theme-safe Streamlit native widgets and feedback panels */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {{ color:{t['text']} !important; }}

[data-baseweb="select"] > div,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {{
    background:{t['surface']} !important;
    color:{t['text']} !important;
    border-color:{t['border']} !important;
}}

[data-testid="stExpander"] {{
    background:{t['surface']} !important;
    border-color:{t['border']} !important;
}}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {{
    color:{t['text']} !important;
}}

[data-testid="stAlert"] {{
    color:{t['text']} !important;
    border:1px solid {t['border']} !important;
}}



/* V25 compact two-card flight board */
.compact-flight {{
    display:grid !important;
    grid-template-columns: 1fr auto !important;
    gap:4px 8px !important;
    padding:9px 10px !important;
    min-height:118px !important;
    align-items:center !important;
}}
.compact-flight .fid {{ grid-column:1; font-size:.92rem !important; }}
.compact-flight .route {{ grid-column:1 / -1; font-size:.9rem !important; font-weight:700; }}
.compact-flight .timing {{ grid-column:1 / -1; font-size:.72rem !important; color:{t['muted']}; }}
.compact-flight .info {{ grid-column:1; font-size:.72rem !important; }}
.compact-flight .badge {{ grid-column:2; grid-row:1; min-width:68px !important; min-height:30px !important; font-size:.7rem !important; }}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>🖥 Operations Control Center</h1><p>Multi-agent disruption management · Single operational source of truth</p></div>', unsafe_allow_html=True)

states = get_all_operational_states()

# Compact control bar: navigation, board filter and page selector in one row.
nav_col, filter_col, page_col, spacer_col = st.columns([1.25, 1.55, 1.0, 4.2], vertical_alignment="bottom")
with nav_col:
    if st.button("← Back to Home", key="ops_back", use_container_width=True):
        st.switch_page("app.py")
with filter_col:
    status_filter = st.selectbox(
        "Board status filter",
        ["All", "On Time", "Delayed", "Cancelled"],
        key="board_filter"
    )
board_states = states if status_filter == "All" else [
    x for x in states if x["effective_status"] == status_filter
]
page_size = 6
pages = max(1, (len(board_states) + page_size - 1) // page_size)
with page_col:
    page = st.selectbox("Board page", list(range(1, pages + 1)), key="board_page")
start = (int(page) - 1) * page_size
shown = board_states[start:start + page_size]
weather = {}
for s in states:
    ap = s.get("affected_airport") or s["origin"]
    if s.get("weather") and ap not in weather: weather[ap] = s["weather"]
# include all weather airports
import json
import random
import string
DATA_DIR=os.path.join(os.path.dirname(__file__),"..","..","mock_data")
with open(os.path.join(DATA_DIR,"weather.json")) as f: weather=json.load(f)

delayed=sum(s['effective_status']=='Delayed' for s in states); cancelled=sum(s['effective_status']=='Cancelled' for s in states); high=sum(w['severity']=='HIGH' for w in weather.values())
cols=st.columns(4)
for c,val,label in zip(cols,[len(states),delayed,cancelled,high],["Total Flights","Delayed","Cancelled","High-Risk Airports"]):
    c.markdown(f'<div class="metric"><div class="l">{label}</div><div class="v">{val}</div></div>',unsafe_allow_html=True)

left,right=st.columns(2)
with left:
    st.markdown('<div class="section">Airport Weather Status</div>',unsafe_allow_html=True)
    for ap,w in weather.items():
        sev=w['severity']; cls=sev.lower()
        st.markdown(f'<div class="weather {cls}"><div><div class="ap">{ap}</div><div class="wd">{w["condition"]} · Wind {w["wind_knots"]} kts · Vis {w["visibility_miles"]} mi</div></div><span class="badge b-{cls}">{sev}</span></div>',unsafe_allow_html=True)
with right:
    st.markdown('<div class="section">Live Flight Board</div>',unsafe_allow_html=True)
    for row_start in range(0, len(shown), 2):
        board_cols=st.columns(2)
        for offset, s in enumerate(shown[row_start:row_start+2]):
            status=s['effective_status']; cls=status.lower().replace(' ','')
            dep=s.get("scheduled_departure","")[11:16]; arr=s.get("scheduled_arrival","")[11:16]
            timing=f"Dep {dep} · Arr {arr}"
            if status=="Delayed" and s.get("estimated_departure"):
                timing += f" · Est {s['estimated_departure'][11:16]}"
            with board_cols[offset]:
                st.markdown(
                    f'<div class="flight compact-flight">'
                    f'<span class="fid">{s["flight_id"]}</span>'
                    f'<span class="route">{s["origin"]} → {s["destination"]}</span>'
                    f'<span class="timing">{timing}</span>'
                    f'<span class="info">{s.get("operational_stage","At Gate")} · {s.get("current_location",s["origin"])}</span>'
                    f'<span class="badge b-{cls}">{status}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

st.markdown('<div class="section">AI Disruption Analysis</div>',unsafe_allow_html=True)
selected=st.selectbox("Select Flight",[s['flight_id'] for s in states],key='analysis_flight')
state=get_operational_state(selected)
if st.session_state.get('selected_state_flight') != selected:
    st.session_state.pop('ops_result',None); st.session_state['selected_state_flight']=selected

status=state['effective_status']

# Demo-only scenario tools stay collapsed so the operational workflow remains clean.
with st.expander("🎬 Demo Tools", expanded=False):
    st.caption("Generate a passenger for the selected flight, then test the same PNR from the Passenger portal.")
    demo_c1, demo_c2 = st.columns([1.5, 4.5], vertical_alignment="bottom")
    with demo_c1:
        create_demo_pnr = st.button(
            "＋ Generate Demo PNR",
            use_container_width=True,
            key=f"generate_demo_pnr_{selected}"
        )

    if create_demo_pnr:
        passengers_path=os.path.join(DATA_DIR,"passengers.json")
        with open(passengers_path,"r",encoding="utf-8") as f:
            passenger_records=json.load(f)

        existing_pnrs={p.get("pnr","") for p in passenger_records}
        alphabet=string.ascii_uppercase + string.digits
        while True:
            new_pnr="".join(random.choices(alphabet,k=6))
            if new_pnr not in existing_pnrs:
                break

        passenger_number=len(passenger_records)+1
        new_passenger={
            "pnr":new_pnr,
            "passenger_name":f"Demo Passenger {passenger_number}",
            "flight_id":selected,
            "email":f"demo{passenger_number}@example.com",
            "phone":f"+1-555-{passenger_number:04d}",
            "seat":f"{10 + (passenger_number % 20)}{chr(65 + passenger_number % 6)}",
            "cabin":"Economy Class",
            "terminal":"A",
            "gate":f"{state['origin']}-B{(passenger_number % 12) + 1}"
        }
        passenger_records.append(new_passenger)

        with open(passengers_path,"w",encoding="utf-8") as f:
            json.dump(passenger_records,f,indent=2)

        st.session_state["last_demo_pnr"]={
            "pnr":new_pnr,
            "flight_id":selected,
            "status":status,
            "passenger_name":new_passenger["passenger_name"]
        }

    with demo_c2:
        generated=st.session_state.get("last_demo_pnr")
        if generated and generated.get("flight_id")==selected:
            st.success(
                f"Demo PNR: {generated['pnr']} | Flight: {generated['flight_id']} | "
                f"Status: {generated['status']} | Passenger: {generated['passenger_name']}"
            )
        else:
            st.info("Generate a unique 6-character PNR for this flight, then search it on the Passenger page.")
if status=='On Time':
    st.success(f"✅ {selected} is ON TIME. There is no active delay, cancellation, or recovery exception. No recovery plan is required.")
    a,b=st.columns(2); a.text_input("Affected Airport",value="None",disabled=True); b.text_input("Disruption Cause",value="No Active Disruption",disabled=True)
    submitted=False
else:
    msg=f"{selected} is {status.upper()} · Affected airport: {state['affected_airport']} · Cause: {state['cause']}"
    (st.warning if status=='Delayed' else st.error)(msg)
    a,b=st.columns(2); a.text_input("Affected Airport",value=state['affected_airport'],disabled=True); b.text_input("Disruption Cause",value=state['cause'],disabled=True)
    submitted=st.button("▶ Run AI Analysis",type="primary",use_container_width=True)

if submitted:
    with st.spinner("Agents are analyzing the disruption..."):
        started=time.time()
        try:
            r=httpx.post("http://localhost:8001/analyze",json={"flight_id":selected},timeout=60)
            r.raise_for_status(); result=r.json(); st.session_state.ops_result=result; st.session_state.ops_elapsed=round(time.time()-started,1)
        except Exception as e: st.error(f"API error: {e}. Start the bridge with: python dashboard/api_bridge.py")

result=st.session_state.get('ops_result')
if result and result.get('flight_id')==selected:
    st.success(f"Analysis completed in {st.session_state.get('ops_elapsed',0)} seconds · Recovery Plan {'APPROVED' if result.get('plan_approved') else 'REVIEW REQUIRED'}")
    tabs=st.tabs(["🌩 Weather Agent","📊 Prediction Agent","🔧 Recovery Agent","✅ Evaluator Agent","📢 Comms Agent"])

    recovery_path=os.path.join(DATA_DIR,"recovery_state.json")
    try:
        with open(recovery_path,"r",encoding="utf-8") as f:
            current_recovery_state=json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        current_recovery_state={}

    applied_records=[
        dict({"pnr":pnr},**rec)
        for pnr,rec in current_recovery_state.items()
        if rec.get("original_flight")==selected and rec.get("applied")
    ]

    with tabs[0]:
        st.markdown("#### Weather Report")
        st.markdown(result.get("weather",""))

    with tabs[1]:
        st.markdown("#### Prediction Report")
        st.markdown(result.get("prediction",""))

    with tabs[2]:
        if applied_records:
            first=applied_records[0]
            st.markdown("#### ✅ Applied Recovery")
            st.success("This recovery plan is applied and synchronized with Passenger and Communications views.")
            c1,c2,c3,c4=st.columns(4)
            c1.metric("Original Flight",selected)
            c2.metric("Recovery Flight",first.get("new_flight","Pending"))
            c3.metric("New Gate",first.get("new_gate","Pending"))
            c4.metric("Passengers Rebooked",len(applied_records))
            st.markdown(f"""
**New departure:** {first.get('new_departure','Pending').replace('T',' ')}  
**Crew assignment:** Recovery crew assigned and operationally cleared  
**Cabin crew status:** Confirmed for recovery departure  
**Ground team:** Gate transfer and baggage rerouting notified  
**Recovery status:** Confirmed
""")
        else:
            st.markdown("#### Proposed Recovery")
            st.info("This is a proposed recovery plan. Apply it to synchronize Recovery, Communications and Passenger views.")
            st.markdown(result.get("recovery_plan",""))

    with tabs[3]:
        st.markdown("#### Evaluation")
        st.markdown(result.get("evaluation",""))

    with tabs[4]:
        st.markdown("#### Communications")
        if applied_records:
            first=applied_records[0]
            dep=first.get("new_departure","Pending").replace("T"," ")
            st.success("Communications updated from the applied recovery record.")
            st.markdown(f"""
**Passenger Communication**

Flight **{selected}** is affected due to **{state.get('cause','an operational disruption')}**. Your recovery has been confirmed on **{first.get('new_flight','Pending')}**, departing at **{dep}** from **Gate {first.get('new_gate','Pending')}**. Seat assignments and meal-voucher details are available through PNR search.

**Staff Communication**

Recovery for **{selected}** is now active. **{len(applied_records)} passenger booking(s)** have been synchronized to recovery flight **{first.get('new_flight','Pending')}**. Crew assignment is confirmed, ground teams have been notified of the gate transfer, and passenger communications are synchronized with the applied recovery record.
""")
        else:
            st.warning("Recovery has not been applied yet. The message below is the pre-recovery disruption communication.")
            st.markdown(result.get("passenger_notification",""))
    metrics=result.get('impact_metrics',{})
    if metrics:
        st.markdown('<div class="section">Simulated Operational Impact</div>',unsafe_allow_html=True)
        cs=st.columns(5)
        vals=[metrics.get('affected_passengers'),metrics.get('alternate_options'),metrics.get('connections_protected'),f"{metrics.get('decision_time_seconds')}s",f"{metrics.get('simulated_time_saved_minutes')}m"]
        labs=["Passengers Affected","Alternate Options","Connections Protected","Decision Time","Simulated Time Saved"]
        for c,v,l in zip(cs,vals,labs): c.markdown(f'<div class="impact"><strong>{v}</strong><span>{l}</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="section">Recovery Plan</div>',unsafe_allow_html=True)
    if st.button("⚡ Apply Recovery Plan",type="primary",use_container_width=True):
        passengers_path=os.path.join(DATA_DIR,"passengers.json")
        recovery_path=os.path.join(DATA_DIR,"recovery_state.json")
        with open(passengers_path,"r",encoding="utf-8") as f:
            passenger_records=json.load(f)
        try:
            with open(recovery_path,"r",encoding="utf-8") as f:
                recovery_state=json.load(f)
        except (FileNotFoundError,json.JSONDecodeError):
            recovery_state={}

        selected_passengers=[p for p in passenger_records if p.get("flight_id")==selected]
        base_departure=state.get("estimated_departure") or state.get("scheduled_departure")
        try:
            recovery_departure=(datetime.fromisoformat(base_departure)+timedelta(hours=2)).isoformat(timespec="minutes")
        except Exception:
            recovery_departure=base_departure or "Pending"

        for idx,p in enumerate(selected_passengers):
            recovery_state[p["pnr"]]={
                "original_flight": selected,
                "new_flight": f"AA{700 + (sum(ord(c) for c in selected) + idx) % 250}",
                "new_departure": recovery_departure,
                "new_gate": f"{state['origin']}-R{(idx % 8) + 1}",
                "seat": p.get("seat","Pending"),
                "voucher_code": f"MEAL-{p['pnr']}" if status in ("Delayed","Cancelled") else None,
                "status": "Confirmed",
                "cause": state.get("cause"),
                "applied": True
            }

        with open(recovery_path,"w",encoding="utf-8") as f:
            json.dump(recovery_state,f,indent=2)

        st.session_state["recovery_applied_for"]=selected
        st.success(f"✅ Recovery Plan applied for {len(selected_passengers)} passenger bookings on {selected}. Recovery Agent, Communications and Passenger PNR views are synchronized.")
        st.rerun()
