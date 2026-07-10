from typing import Any, Dict
from neuro_san.interfaces.coded_tool import CodedTool
from tools.weather_tools import get_mock_weather, get_mock_forecast
from tools.prediction_tools import predict_delay, get_historical_performance, check_aircraft_position
from tools.recovery_tools import search_alternate_flights, get_gate_availability, calculate_passenger_impact
from tools.comms_tools import draft_passenger_message, draft_staff_alert

class WeatherLookup(CodedTool):
    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Any:
        return get_mock_weather(args["airport"])
class ForecastLookup(CodedTool):
    async def async_invoke(self, args, sly_data): return get_mock_forecast(args["airport"])
class DelayPrediction(CodedTool):
    async def async_invoke(self, args, sly_data): return predict_delay(args["flight_id"], args["weather_severity"])
class HistoricalPerformance(CodedTool):
    async def async_invoke(self, args, sly_data): return get_historical_performance(args["route"])
class AircraftPosition(CodedTool):
    async def async_invoke(self, args, sly_data): return check_aircraft_position(args["flight_id"])
class AlternateFlights(CodedTool):
    async def async_invoke(self, args, sly_data): return search_alternate_flights(args["origin"], args["destination"], args.get("date", "2026-07-07"))
class GateAvailability(CodedTool):
    async def async_invoke(self, args, sly_data): return get_gate_availability(args["airport"])
class PassengerImpact(CodedTool):
    async def async_invoke(self, args, sly_data): return calculate_passenger_impact(args["flight_id"], int(args["delay_minutes"]))
class PassengerMessage(CodedTool):
    async def async_invoke(self, args, sly_data): return draft_passenger_message(args["flight_id"], int(args["delay_minutes"]), args["reason"])
class StaffAlert(CodedTool):
    async def async_invoke(self, args, sly_data): return draft_staff_alert(args["flight_id"], args["action"], args["priority"])
