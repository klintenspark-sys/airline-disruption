import json
import os
import re
import sys
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from tools.operational_state import get_operational_state

app = FastAPI(title="Airline Disruption AI API — Neuro SAN Integration")
NEURO_SAN_BASE_URL = os.getenv("NEURO_SAN_BASE_URL", "http://127.0.0.1:8080")
NEURO_SAN_NETWORK = os.getenv("NEURO_SAN_NETWORK", "airline_disruption")

class DisruptionRequest(BaseModel):
    flight_id: str
    airport: str | None = None
    reason: str | None = None

@app.get("/health")
def health():
    neuro_ok = False
    detail = None
    try:
        r = httpx.get(f"{NEURO_SAN_BASE_URL}/api/v1/{NEURO_SAN_NETWORK}/function", timeout=5)
        neuro_ok = r.status_code == 200
        if not neuro_ok: detail = f"HTTP {r.status_code}"
    except Exception as exc:
        detail = str(exc)
    return {"status": "ok" if neuro_ok else "degraded", "mode": "neuro-san-multi-agent", "network": NEURO_SAN_NETWORK, "neuro_san_reachable": neuro_ok, "detail": detail, "port": 8001}

def _extract_final_text(response: httpx.Response) -> str:
    final_text = ""

    for raw in response.iter_lines():
        if not raw:
            continue

        line = raw.strip()

        if line.startswith("data:"):
            line = line[5:].strip()

        try:
            obj = json.loads(line)

            print("=" * 80)
            print("STREAM EVENT:")
            print(json.dumps(obj, indent=2))
            print("=" * 80)

        except json.JSONDecodeError:
            print("NON-JSON:", line)
            continue

        payload = obj.get("response", obj)

        if not isinstance(payload, dict):
            continue

        text = payload.get("text", "")
        msg_type = str(payload.get("type", ""))

        print(f"TYPE: {msg_type}")
        print(f"TEXT: {text}")

        if text:
            stripped = text.strip()

            # Only keep text that looks like JSON
            if stripped.startswith("{") and stripped.endswith("}"):
                final_text = stripped

    if not final_text:
        try:
            obj = response.json()
            payload = obj.get("response", obj)

            if isinstance(payload, dict):
                final_text = payload.get("text", "")
        except Exception:
            pass

    print("=" * 80)
    print("FINAL TEXT")
    print(final_text)
    print("=" * 80)

    return final_text
def _parse_json_text(text: str) -> dict[str, Any]:
    cleaned=text.strip()
    cleaned=re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned=re.sub(r"\s*```$", "", cleaned)
    try: return json.loads(cleaned)
    except json.JSONDecodeError:
        match=re.search(r"\{.*\}", cleaned, flags=re.S)
        if not match: raise ValueError(f"Neuro SAN returned non-JSON final output: {cleaned[:500]}")
        return json.loads(match.group(0))

def _run_neuro_san(prompt: str) -> dict[str, Any]:
    url=f"{NEURO_SAN_BASE_URL}/api/v1/{NEURO_SAN_NETWORK}/streaming_chat"
    try:
        with httpx.stream("POST", url, json={"user_message":{"text":prompt}}, timeout=httpx.Timeout(900.0)) as response:
            response.raise_for_status()
            final_text=_extract_final_text(response)
    except httpx.HTTPError as exc:
        raise RuntimeError(f"Neuro SAN network is unavailable at {url}. Start it with start_neuro_san.ps1. Details: {exc}") from exc
    if not final_text: raise RuntimeError("Neuro SAN completed without a final framework response.")
    return _parse_json_text(final_text)

@app.post("/analyze")
def analyze(req: DisruptionRequest):
    try:
        state=get_operational_state(req.flight_id)
        status=state["effective_status"]
        if status == "On Time":
            return {"status":"complete","framework":"Neuro SAN","flight_status":"On Time","flight_id":req.flight_id,"airport":None,"reason":"No Active Disruption","plan_approved":False,"weather":"No disruption analysis required. The flight is operating normally.","prediction":"Current status: ON TIME. No delay or cancellation exception is active.","recovery_plan":"","evaluation":"Not required — normal operation.","passenger_notification":f"PASSENGER NOTIFICATION\nFlight {req.flight_id} is ON TIME. There are no active disruption exceptions and no recovery action is required. Have a pleasant journey.","impact_metrics":{}}

        airport=req.airport or state["affected_airport"]
        reason=req.reason or state["cause"]
        delay=int(state.get("current_delay_minutes") or 0)
        weather=state.get("weather",{})
        prompt=f'''Analyze airline disruption for flight {req.flight_id}.\nFlight status: {status}\nOrigin: {state['origin']}\nDestination: {state['destination']}\nAffected airport: {airport}\nDisruption reason: {reason}\nCurrent delay minutes: {delay}\nKnown weather severity: {weather.get('severity', state.get('severity','LOW'))}\nCoordinate all specialist agents and return the required JSON object only.'''
        agent_result=_run_neuro_san(prompt)
        impact_metrics={"affected_passengers": state.get("passengers",0), "framework":"Neuro SAN", "agent_network":NEURO_SAN_NETWORK}
        return {"status":"complete","framework":"Neuro SAN","flight_status":status,"flight_id":req.flight_id,"airport":airport,"reason":reason,"weather":str(agent_result.get("weather","")),"prediction":str(agent_result.get("prediction","")),"recovery_plan":str(agent_result.get("recovery_plan","")),"evaluation":str(agent_result.get("evaluation","")),"plan_approved":bool(agent_result.get("plan_approved",False)),"passenger_notification":str(agent_result.get("passenger_notification","")),"impact_metrics":impact_metrics}
    except Exception as exc:
        return JSONResponse(status_code=503, content={"error":str(exc),"framework":"Neuro SAN","hint":"Start Neuro SAN first with start_neuro_san.ps1, then start the API bridge."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
