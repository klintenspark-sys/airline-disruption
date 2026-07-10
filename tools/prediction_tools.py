import json

import random

import os
 
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "mock_data")
 
 
def predict_delay(flight_id: str, weather_severity: str) -> dict:

    severity_map = {"LOW": 0.1, "MEDIUM": 0.5, "HIGH": 0.9}

    prob = severity_map.get(weather_severity.upper(), 0.3) + random.uniform(-0.05, 0.05)

    prob = round(min(prob, 1.0), 2)

    return {

        "flight_id": flight_id,

        "delay_probability": prob,

        "estimated_delay_minutes": random.randint(30, 240) if prob > 0.5 else 0,

        "cascade_risk": "HIGH" if prob > 0.7 else "MEDIUM" if prob > 0.4 else "LOW"

    }
 
 
def get_historical_performance(route: str) -> dict:

    return {

        "route": route,

        "on_time_rate_30d": round(random.uniform(0.6, 0.95), 2),

        "avg_delay_minutes": random.randint(5, 45)

    }
 
 
def check_aircraft_position(flight_id: str) -> dict:

    return {

        "flight_id": flight_id,

        "current_position": random.choice(["At Gate", "Taxiing", "Airborne", "Landed"]),

        "fuel_status": random.choice(["Full", "Partial", "Low"])

    }

 