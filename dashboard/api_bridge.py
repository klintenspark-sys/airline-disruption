import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from tools.operational_state import get_operational_state
from tools.recovery_tools import search_alternate_flights, get_gate_availability, calculate_passenger_impact

app = FastAPI(title="Airline Disruption AI API")

class DisruptionRequest(BaseModel):
    flight_id: str
    airport: str | None = None
    reason: str | None = None

@app.get("/health")
def health():
    return {"status": "ok", "mode": "fast-multi-agent-simulation", "port": 8001}

def score_plan(alternates, gates, affected, status):
    feasibility = 9 if gates else 6
    passenger = 9 if alternates and "message" not in alternates[0] else 6
    cost = 7 if status == "Cancelled" else 8
    compliance = 9
    avg = round((feasibility + passenger + cost + compliance) / 4, 1)
    return feasibility, passenger, cost, compliance, avg

@app.post("/analyze")
def analyze(req: DisruptionRequest):
    try:
        state = get_operational_state(req.flight_id)
        status = state["effective_status"]
        if status == "On Time":
            return {
                "status":"complete", "flight_status":"On Time", "flight_id":req.flight_id,
                "airport":None, "reason":"No Active Disruption", "plan_approved":False,
                "weather":"No disruption analysis required. The flight is operating normally.",
                "prediction":"Current status: ON TIME. No delay or cancellation exception is active.",
                "recovery_plan":"", "evaluation":"Not required — normal operation.",
                "passenger_notification":f"PASSENGER NOTIFICATION\nFlight {req.flight_id} is ON TIME. There are no active disruption exceptions and no recovery action is required. Have a pleasant journey.",
                "impact_metrics":{}
            }
        airport=state["affected_airport"]; reason=state["cause"]; delay=state["current_delay_minutes"]
        weather=state.get("weather", {})
        alts=search_alternate_flights(state["origin"], state["destination"], "2026-07-07")
        gates=get_gate_availability(airport)
        impact=calculate_passenger_impact(req.flight_id, delay if delay else 180)
        affected=impact["affected_passengers"]
        weather_report=(f"- Airport: {airport}\n- Condition: {weather.get('condition','Operational event')}\n"
                        f"- Severity: {weather.get('severity',state.get('severity','LOW'))}\n- Event cause: {reason}")
        if status == "Delayed":
            prediction=(f"- Current status: DELAYED\n- Current delay: {delay} minutes\n"
                        f"- Escalation threshold: {state.get('escalation_threshold_minutes',180)} minutes\n"
                        f"- Cause: {reason}")
            recovery=(f"1. Keep {req.flight_id} in DELAYED status while recovery is active.\n"
                      f"2. Protect seats on {len(alts)} alternate option(s).\n3. Coordinate {len(gates)} available gate option(s).\n"
                      f"4. Validate crew legality and aircraft readiness.\n5. Reassess before the 180-minute escalation threshold.")
        else:
            prediction=(f"- Current status: CANCELLED\n- Cause: {reason}\n- Rebooking and passenger recovery are required.")
            recovery=(f"1. Confirm cancellation of {req.flight_id}.\n2. Rebook passengers using {len(alts)} alternate option(s).\n"
                      f"3. Coordinate gate, baggage and crew reassignment.\n4. Protect connecting passengers.\n5. Notify all {affected} passengers and staff.")
        feasibility, passenger, cost, compliance, avg=score_plan(alts,gates,affected,status)
        approved=avg>=7
        evaluation=(f"- Feasibility: {feasibility}/10\n- Passenger Impact: {passenger}/10\n- Cost: {cost}/10\n"
                    f"- Compliance: {compliance}/10\n- Average: {avg}/10\n- Decision: {'APPROVED' if approved else 'REJECTED'}")
        if status=='Delayed':
            pax=f"Flight {req.flight_id} is DELAYED by approximately {delay} minutes due to {reason}. Recovery actions are active and updated departure details will be communicated when confirmed."
            staff=f"Flight {req.flight_id} remains DELAYED. Continue gate, crew and passenger recovery coordination for {affected} passengers."
        else:
            pax=f"Flight {req.flight_id} has been CANCELLED due to {reason}. Rebooking and recovery actions are in progress. Please review your updated itinerary."
            staff=f"Flight {req.flight_id} is CANCELLED. Begin rebooking, gate, baggage, crew and communication actions for {affected} passengers."
        metrics={
            "affected_passengers": affected, "alternate_options": len(alts),
            "connections_protected": impact.get("missed_connections",0),
            "decision_time_seconds": 2, "estimated_manual_minutes": 35,
            "simulated_time_saved_minutes": 33
        }
        return {"status":"complete","flight_status":status,"flight_id":req.flight_id,"airport":airport,"reason":reason,
                "weather":weather_report,"prediction":prediction,"recovery_plan":recovery,"evaluation":evaluation,
                "plan_approved":approved,"passenger_notification":f"PASSENGER NOTIFICATION\n{pax}\n\nSTAFF ALERT\n{staff}",
                "impact_metrics":metrics}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error":str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
