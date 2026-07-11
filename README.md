✈️ AI-Powered Airline Disruption Management Platform
====================================================

An interactive multi-agent airline disruption management prototype built for hackathon demonstration. The platform connects airline operations analysis, disruption recovery, communication, and passenger self-service through a shared operational state.

The application provides two coordinated experiences:

- **Operations Control Center** — monitor flights, review airport weather, analyze disruptions, evaluate recovery options, apply recovery plans, and generate synchronized communications.
- **Passenger Portal** — search by PNR to view current flight status and confirmed recovery details.

See [`architecture.md`](./architecture.md) for a full breakdown of the agentic system design, and [`summary.md`](./summary.md) for a project overview.

## Primary AI Framework: Neuro SAN Studio

Neuro SAN Studio is the primary multi-agent orchestration framework for disruption analysis. Streamlit is the presentation layer, while a FastAPI bridge submits disrupted-flight context to the `airline_disruption` Neuro SAN agent network. The network is defined declaratively in HOCON and coordinates Weather, Prediction, Recovery, Evaluator, and Communications agents. Grounded operational functions are exposed to those agents as Neuro SAN CodedTools.

The live analysis path is:

```
Streamlit → API Bridge → Neuro SAN → Specialist Agents → CodedTools → Structured Result → UI
```

## Project structure

```
airline-disruption/
├── agents/               # Agent role definitions
├── coded_tools/          # Grounded operational functions exposed to agents
├── dashboard/            # Streamlit UI (Operations Control Center + Passenger Portal)
├── logs/                 # Runtime logs
├── mock_data/            # Seed flight data + recovery_state.json (persisted recovery records)
├── registries/           # HOCON agent network declarations
├── tools/                # Supporting utilities
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── start_bridge.ps1       # Launches the FastAPI bridge
├── start_dashboard.ps1    # Launches the Streamlit dashboard
├── start_neuro_san.ps1    # Launches the Neuro SAN agent network server
├── architecture.md        # Agentic system architecture
├── summary.md             # Project summary
└── README.md               # This file
```

## Prerequisites

- Python 3.10+
- PowerShell (the provided `start_*.ps1` scripts are PowerShell; on macOS/Linux use PowerShell Core (`pwsh`), or run the equivalent commands directly — see below)
- pip

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/klintenspark-sys/airline-disruption.git
   cd airline-disruption
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` to `.env` (if present) and set any required values, e.g. your LLM provider API key and the Neuro SAN network name (`airline_disruption`). Check `config.py` for the full list of settings the app reads.

## Running the application

The platform has three services that need to run concurrently: the Neuro SAN agent network, the FastAPI bridge, and the Streamlit dashboard.

**Using the provided scripts (PowerShell / Windows):**

```powershell
# Terminal 1 — start the Neuro SAN agent network
./start_neuro_san.ps1

# Terminal 2 — start the FastAPI bridge
./start_bridge.ps1

# Terminal 3 — start the Streamlit dashboard
./start_dashboard.ps1
```

**Equivalent manual commands (macOS/Linux/any shell):**

```bash
# Terminal 1 — Neuro SAN agent network
python -m neuro_san.run --config registries/airline_disruption.hocon

# Terminal 2 — FastAPI bridge
uvicorn dashboard.bridge:app --reload --port 8000

# Terminal 3 — Streamlit dashboard
streamlit run dashboard/app.py
```

> Adjust module/file paths above to match your actual entry points if they differ — check each `start_*.ps1` script for the exact command it runs.

Once all three are running, open the Streamlit URL printed in Terminal 3 (typically `http://localhost:8501`) to access:

- **Operations Control Center:** `http://localhost:8501/Ops_Team`
- **Passenger Portal:** `http://localhost:8501/Passenger`

## Using the demo

1. From the **Operations Control Center**, review the live flight board and airport weather status.
2. Select a disrupted flight and trigger the multi-agent analysis.
3. Review the recovery proposal once the Weather → Prediction → Recovery → Evaluator pipeline completes.
4. Click **Apply Recovery Plan** to commit and persist the recovery.
5. Copy the flight's PNR and switch to the **Passenger Portal** to see the confirmed recovery — new flight, gate, seat, and voucher — from the passenger's point of view.

## Recovery records

Applied recovery information is stored in `mock_data/recovery_state.json` and can include: original flight, recovery flight, new departure time, new gate, seat, voucher information, and confirmation status. Resetting a PNR search clears the Passenger Portal's display state but does **not** delete the persisted recovery booking.

## Further reading

- [`architecture.md`](./architecture.md) — agentic system architecture, data flow, and the Sly-Data mechanism
- [`summary.md`](./summary.md) — project summary
- `NEURO_SAN_INTEGRATION.md` — Neuro SAN-specific integration notes
