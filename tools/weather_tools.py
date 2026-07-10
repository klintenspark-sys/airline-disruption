import json
import os
 
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "mock_data")
 
 
def get_mock_weather(airport_code: str) -> dict:
    with open(os.path.join(DATA_DIR, "weather.json")) as f:
        weather = json.load(f)
    return weather.get(airport_code.upper(), {"condition": "Unknown", "severity": "LOW"})
 
 
def get_mock_forecast(airport_code: str) -> list:
    import random
    conditions = ["Clear", "Cloudy", "Rain", "Thunderstorm"]
    return [{"hour": i, "condition": random.choice(conditions)} for i in range(1, 7)]