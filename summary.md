# Project Summary

## The problem

Every year, millions of passengers experience the chaotic ripple effects of flight disruptions. Recovering from a disruption — a weather event, a ground stop, a maintenance issue — requires coordination across weather data, delay prediction, recovery planning, and passenger communication. Traditional systems fail here because they rely on fragmented information across disconnected tools, resulting in slow decisions, inconsistent recovery actions, and contradictory communication to passengers and staff.

## The solution

We built an **AI-Powered Airline Disruption Management Platform** — an interactive multi-agent prototype that connects operations analysis, disruption recovery, communication, and passenger self-service through one shared operational state.

The platform is orchestrated by **Cognizant Neuro SAN Studio**, running a network of agents declared in HOCON against a **local Ollama LLM**. An orchestrator agent coordinates five specialists in sequence:

- The **Weather Agent** assesses current conditions and a six-hour outlook for the affected airport.
- The **Prediction Agent** estimates delay probability and cascade risk.
- The **Recovery Agent** builds a concrete recovery proposal — alternate flight, gate, and passenger impact — grounded in real lookup data rather than invented facts, and is explicitly instructed to never silently escalate a delay into a cancellation.
- The **Evaluator Agent** independently scores the proposal on feasibility, passenger impact, cost efficiency, and compliance, approving it only if the average score clears a threshold.
- The **Communications Agent** drafts passenger and staff messaging that must match the actual flight status — never describing a delayed or cancelled flight as on-time.

Operational facts (flights, weather, gates, passengers) are exposed to the agents as grounded **CodedTools** backed by mock JSON data, so the LLM looks facts up rather than guessing them.

## How it works, end to end

Dispatchers work from an **Operations Control Center**: a live flight board and airport weather overview. Selecting a disrupted flight and running the AI analysis sends the flight's context through a FastAPI bridge to the Neuro SAN agent network, which runs the full weather → prediction → recovery → evaluation → communications sequence and returns one structured result.

The system does **not** auto-execute. The operator reviews the recovery proposal — including the evaluator's approval score — and only when they click **Apply Recovery Plan** is the change committed and persisted.

That persisted state is what powers the **Passenger Portal**: a traveler searching their PNR resolves their itinerary against the same recovery state the operator just applied, instantly seeing their new flight, gate, seat, and voucher — with no risk of stale or conflicting information, since the Communications Agent only ever drafts messaging from the final, applied decision.

If a bridge request finds Neuro SAN unreachable, it deliberately returns an error rather than falling back to fake data — the demo can't silently mask a broken agent network.

## What this demonstrates

This project is a working blueprint for dividing a complex, high-stakes operational workflow into focused, auditable agent roles that share state consistently, with an explicit evaluation gate and a human operator firmly in the loop before anything is applied. The agent network is declared, not hardcoded, so additional specialists (crew legality, gate-conflict analysis) could be added without restructuring the orchestration layer.

## Tech stack

- **Orchestration:** Cognizant Neuro SAN Studio (HOCON-declared agent network)
- **LLM:** Ollama, local, configured per-network in HOCON
- **Frontend:** Python + Streamlit
- **Integration layer:** FastAPI bridge between the UI and the agent network
- **State persistence:** Local JSON files (no database dependency for the prototype)

## Key takeaway

By separating **proposed** recovery from **applied** recovery, gating that transition on an independent evaluator score, and keeping a human operator in control of execution, the platform shows that a multi-agent system can be both fast and auditable — turning a multi-step coordination problem into a single, consistent source of operational truth that both operations staff and passengers read from.

## Current scope & disclaimer

This is a hackathon prototype using mock, locally-generated data (`mock_data/`) and local JSON persistence — it is not connected to a live airline reservation, operations-control, or notification system. Future enhancements under consideration include real-time flight/weather APIs, database-backed persistence, authentication, and agent execution tracing (see the repo README for the full list).
