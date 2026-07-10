import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "mock_data")

def _load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)

def get_operational_state(flight_id: str) -> dict:
    flights = _load("flights.json")
    disruptions = _load("disruptions.json")
    weather = _load("weather.json")
    flight = next((f for f in flights if f["flight_id"] == flight_id), None)
    if not flight:
        raise ValueError(f"Unknown flight: {flight_id}")
    event = disruptions.get(flight_id)
    if not event or not event.get("event_active"):
        return {
            **flight, "event_active": False, "effective_status": "On Time",
            "affected_airport": None, "cause": None, "current_delay_minutes": 0,
            "recovery_required": False, "weather": weather.get(flight["origin"], {})
        }
    status = event["status"]
    delay = int(event.get("current_delay_minutes", 0) or 0)
    threshold = int(event.get("escalation_threshold_minutes", 180))
    if status == "Delayed" and delay >= threshold:
        status = "Cancelled"
    airport = event["affected_airport"]
    return {**flight, **event, "effective_status": status, "weather": weather.get(airport, {})}

def get_all_operational_states() -> list:
    return [get_operational_state(f["flight_id"]) for f in _load("flights.json")]
