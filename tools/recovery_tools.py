import json
import random
import os
 
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "mock_data")
 
 
def search_alternate_flights(origin: str, destination: str, date: str) -> list:
    with open(os.path.join(DATA_DIR, "flights.json")) as f:
        flights = json.load(f)
    alts = [f for f in flights if f["origin"] == origin.upper() and f["destination"] == destination.upper()]
    return alts[:3] if alts else [{"message": "No alternates found on this route"}]
 
 
def check_crew_legality(crew_id: str, flight_hours: int) -> dict:
    with open(os.path.join(DATA_DIR, "crew.json")) as f:
        crew = json.load(f)
    member = next((c for c in crew if c["crew_id"] == crew_id), None)
    if not member:
        return {"legal": False, "reason": "Crew member not found"}
    legal = member["hours_remaining"] >= flight_hours and member["available"]
    return {
        "crew_id": crew_id,
        "name": member["name"],
        "legal": legal,
        "hours_remaining": member["hours_remaining"],
        "available": member["available"]
    }
 
 
def get_gate_availability(airport: str) -> list:
    with open(os.path.join(DATA_DIR, "gates.json")) as f:
        gates = json.load(f)
    available = [g for g in gates.get(airport.upper(), []) if g["available"]]
    return available[:5]
 
 
def calculate_passenger_impact(flight_id: str, delay_minutes: int) -> dict:
    with open(os.path.join(DATA_DIR, "flights.json")) as f:
        flights = json.load(f)
    flight = next((f for f in flights if f["flight_id"] == flight_id), {})
    passengers = flight.get("passengers", 150)
    return {
        "flight_id": flight_id,
        "affected_passengers": passengers,
        "missed_connections": round(passengers * 0.15),
        "compensation_estimate_usd": passengers * (delay_minutes // 60) * 12,
        "rebooking_required": delay_minutes > 120
    }