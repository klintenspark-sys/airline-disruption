def draft_passenger_message(flight_id: str, delay_minutes: int, reason: str) -> str:
    return (
        f"Dear Passengers of Flight {flight_id},\n\n"
        f"We regret to inform you that your flight has been delayed by approximately "
        f"{delay_minutes} minutes due to {reason}.\n\n"
        f"Our team is working to minimize the impact and will provide updates every 30 minutes.\n"
        f"Meal vouchers are available at the gate for delays exceeding 2 hours.\n\n"
        f"We apologize for the inconvenience and appreciate your patience.\n\n"
        f"— Airline Operations Team"
    )
 
 
def draft_staff_alert(flight_id: str, action: str, priority: str) -> dict:
    return {
        "type": "STAFF_ALERT",
        "flight": flight_id,
        "action_required": action,
        "priority": priority,
        "timestamp": "2026-07-07T10:00:00Z",
        "departments": ["Ground Crew", "Gate Agents", "Customer Service"]
    }