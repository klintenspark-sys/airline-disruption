# Architecture

## What this project does

The **AI-Powered Airline Disruption Management Platform** coordinates the time-critical work of recovering from flight disruptions — weather delays, ground stops, cancellations — across weather assessment, delay prediction, recovery planning, plan evaluation, and passenger/staff communication.

Rather than asking a single LLM call to reason about all of this at once, the platform delegates the workflow across a network of agents orchestrated by **Cognizant Neuro SAN Studio**, running against a **local Ollama LLM**. Each agent has a narrow, well-defined responsibility, and an explicit evaluation step sits between "plan proposed" and "plan executed."

## The agent network

Agents are declared in `registries/airline_disruption.hocon` and served by Neuro SAN Studio (`start_neuro_san.ps1`, port `8080`). The network consists of one orchestrator and five specialists:

| Agent | Role | Coded tools it calls |
|---|---|---|
| **orchestrator** | The "frontman." Coordinates the full analysis in a fixed sequence — weather → prediction → recovery → evaluator → comms — and returns one structured JSON result (`weather`, `prediction`, `recovery_plan`, `evaluation`, `plan_approved`, `passenger_notification`). | *(delegates to the five specialists below)* |
| **weather_agent** | Assesses current conditions and a six-hour outlook for the affected airport. | `weather_lookup`, `forecast_lookup` |
| **prediction_agent** | Assesses delay probability and cascade risk for the flight. | `delay_prediction`, `historical_performance`, `aircraft_position` |
| **recovery_agent** | Builds a grounded recovery proposal (alternate flight, gate, passenger impact). Instructed to preserve `DELAYED` status unless the source status is genuinely `CANCELLED` — it must not silently upgrade a delay into a cancellation. | `alternate_flights`, `gate_availability`, `passenger_impact` |
| **evaluator_agent** | Scores the recovery proposal on feasibility, passenger impact, cost efficiency, and compliance (1–10 each), averages them, and returns **APPROVED** if the average is ≥ 7, otherwise **REJECTED** with corrective feedback. | *(no tools — LLM judgment only)* |
| **comms_agent** | Drafts passenger and staff messaging that must match the actual flight status — it's explicitly instructed not to describe a delayed/cancelled flight as on-time. | `passenger_message`, `staff_alert` |

The orchestrator's call order is **fixed**, not dynamically negotiated — each specialist runs in sequence and hands its output forward. This keeps the flow predictable and auditable, at the cost of the fully dynamic task delegation that a more open-ended AAOSA network could support.

## LLM configuration

The network runs against a local model via **Ollama**, configured directly in the HOCON:

```hocon
"llm_config": {
  "class": "ollama",
  "model_name": "qwen2.5:3b",
  "base_url": "http://127.0.0.1:11434",
  "temperature": 0.2
}
```

> **Note:** the Streamlit landing page displays `llama3.1:8b` as the "powered by" model, and `config.py` defaults `OLLAMA_MODEL` to `llama3.1:8b` — but the agent network's actual behavior is controlled by the HOCON above, which is hardcoded to `qwen2.5:3b`. These aren't currently wired together; if you change the model, update the HOCON (the source of truth for what the agents actually run on), not just `config.py`.

## Coded tools

Grounded, deterministic operations are exposed to the agents as Neuro SAN **CodedTools** (`coded_tools/airline_tools.py`), which each wrap a plain Python function from `tools/`:

| Tool class | Backing function | Module |
|---|---|---|
| `WeatherLookup` | `get_mock_weather` | `tools/weather_tools.py` |
| `ForecastLookup` | `get_mock_forecast` | `tools/weather_tools.py` |
| `DelayPrediction` | `predict_delay` | `tools/prediction_tools.py` |
| `HistoricalPerformance` | `get_historical_performance` | `tools/prediction_tools.py` |
| `AircraftPosition` | `check_aircraft_position` | `tools/prediction_tools.py` |
| `AlternateFlights` | `search_alternate_flights` | `tools/recovery_tools.py` |
| `GateAvailability` | `get_gate_availability` | `tools/recovery_tools.py` |
| `PassengerImpact` | `calculate_passenger_impact` | `tools/recovery_tools.py` |
| `PassengerMessage` | `draft_passenger_message` | `tools/comms_tools.py` |
| `StaffAlert` | `draft_staff_alert` | `tools/comms_tools.py` |

This separates the agents' *reasoning* (what to do) from *grounded facts* (mock flight, weather, gate, and passenger data drawn from the JSON files in `mock_data/`) — the LLM isn't asked to invent operational data it can look up instead.

Each tool's `async_invoke` signature includes a `sly_data` parameter, which is Neuro SAN's mechanism for passing data between agents outside the visible conversation stream. In the current implementation this parameter is accepted but not populated — all tool calls run on `args` alone. It's available as a hook for a future enhancement (e.g., passing PNR/passenger identity out-of-band) but isn't part of the active data flow today.

## End-to-end data flow

```
Streamlit UI (Operations Control Center, port 8501)
        │  operator selects a disrupted flight, clicks "Run AI Analysis"
        ▼
FastAPI Bridge (dashboard/api_bridge.py, port 8001)
        │  tools/operational_state.py resolves flight + weather + disruption
        │  context from mock_data/*.json into a plain-text prompt
        ▼
POST http://127.0.0.1:8080/api/v1/airline_disruption/streaming_chat
        ▼
Neuro SAN Studio server (port 8080) — registries/airline_disruption.hocon
        │
        ▼
  orchestrator ──▶ weather_agent ──▶ prediction_agent ──▶ recovery_agent ──▶ evaluator_agent ──▶ comms_agent
        │
        ▼
  Single structured JSON result (weather, prediction, recovery_plan,
  evaluation, plan_approved, passenger_notification)
        │
        ▼
Bridge parses the final JSON and returns it to Streamlit
        │
        ▼
Operator reviews the proposal, clicks "Apply Recovery Plan"
        │
        ▼
Recovery committed to mock_data/recovery_state.json
        │
        ▼
Passenger Portal (port 8501/Passenger) reads the same persisted
recovery state via PNR search
```

If the flight's `effective_status` is already **On Time**, the bridge short-circuits and returns a static "no disruption" response without calling Neuro SAN at all — the agent network only runs for genuinely disrupted flights.

The bridge **does not fall back to simulated output** if Neuro SAN is unreachable: `/analyze` returns HTTP 503 with a hint to start `start_neuro_san.ps1`, so a broken agent network can't silently be masked by fake data during a demo.

## Proposed vs. applied recovery

The application explicitly separates a **proposed recovery** (the orchestrator's structured result, gated by the evaluator's APPROVED/REJECTED score) from an **applied recovery** (what the Operations Team has actually confirmed by clicking **Apply Recovery Plan**). Only the applied recovery is:

1. Committed and persisted to `mock_data/recovery_state.json`, and
2. Visible to the Passenger Portal via PNR search.

Resetting a PNR search clears the Passenger Portal's *display* state but does not delete the underlying persisted recovery booking — the two are intentionally decoupled.

## Why this agent split

Weather interpretation, delay prediction, recovery planning, policy evaluation, and communication are different reasoning tasks with different constraints. Dividing them into separate agents:

- Makes each intermediate decision visible and independently inspectable, instead of one opaque end-to-end completion.
- Lets the recovery proposal be scored by a separate evaluator agent before anything is applied.
- Keeps communication strictly downstream of the applied operational decision, preventing messaging that contradicts what actually happened.
- Makes the workflow easier to extend — a new specialist (e.g., a crew-legality agent) can be added to the HOCON and slotted into the orchestrator's sequence without restructuring the rest of the system.

The value isn't the number of agents — it's the coordinated workflow and the single shared operational state (`mock_data/`) that every agent and both UI experiences read from and write to consistently.

## Tech stack by layer

| Layer | Technology |
|---|---|
| Orchestration | Cognizant Neuro SAN Studio (HOCON-declared agent network) |
| LLM | Ollama, local (`qwen2.5:3b` per the HOCON config) |
| Frontend | Python + Streamlit (`dashboard/app.py`, `dashboard/pages/`) |
| Integration | FastAPI bridge (`dashboard/api_bridge.py`, port 8001) |
| Agent-exposed operations | Neuro SAN CodedTools (`coded_tools/airline_tools.py`) |
| State persistence | Local JSON (`mock_data/*.json`, notably `recovery_state.json`) |
