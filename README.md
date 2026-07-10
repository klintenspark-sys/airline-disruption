# AI-Powered Airline Disruption Management Platform

A multi-agent airline disruption management platform that connects
operational monitoring, disruption analysis, recovery planning,
evaluation, communication, and passenger self-service through a shared
operational state.

## Overview

Airline disruptions require coordinated decisions across weather
monitoring, operations, recovery planning, crew and passenger handling,
and communications. This project demonstrates a coordinated workflow in
which specialized AI agents divide those responsibilities while using
consistent operational and recovery data.

The application provides two connected experiences:

-   **Operations Control Center** --- monitors flights and airport
    conditions, analyzes disruptions, reviews recovery proposals,
    applies recovery plans, and generates synchronized communications.
-   **Passenger Portal** --- allows passengers to search by PNR and view
    current flight information and confirmed recovery details.

## Core Workflow

``` text
Flight and Airport Operational Data
                ↓
        Disruption Analysis
                ↓
   Weather and Impact Assessment
                ↓
         Recovery Proposal
                ↓
        Recovery Evaluation
                ↓
       Human-Controlled Apply
                ↓
      Shared Recovery State
           ↙           ↘
 Communications     Passenger Portal
```

## Multi-Agent Workflow

The platform separates the disruption-management process into
specialized responsibilities:

1.  **Weather Agent** --- evaluates weather and environmental conditions
    affecting operations.
2.  **Prediction Agent** --- estimates disruption impact and delay risk.
3.  **Recovery Agent** --- creates a recovery proposal using the flight
    and disruption context.
4.  **Evaluator Agent** --- reviews the proposed recovery before
    execution.
5.  **Communications Agent** --- prepares passenger and staff messages
    using the operational decision.

The objective is not simply to use multiple agents. The architecture
divides responsibilities, exposes intermediate decisions, supports
evaluation before execution, and keeps downstream communication aligned
with the applied recovery state.

## Key Features

### Operations Control Center

-   Airport weather status overview
-   Live flight board with pagination
-   Flight status filtering
-   On Time, Delayed, and Cancelled states
-   Scheduled and estimated flight timing
-   Operational stage and current location
-   Automatic affected-airport and disruption-cause selection
-   Multi-agent disruption analysis
-   Recovery proposal and evaluation
-   Controlled recovery-plan application
-   Applied recovery details including flight, departure time, gate,
    passenger impact, crew status, and ground-team status
-   Passenger and staff communication synchronized with applied recovery
    details
-   Demo Tools for generating a unique PNR linked to the selected flight

### Passenger Portal

-   PNR-based booking search
-   Dynamic passenger and flight information
-   Current flight status
-   Confirmed recovery booking details
-   Recovery flight, departure time, gate, and seat information
-   Voucher and notification information where applicable
-   Reset PNR functionality
-   Recovery information synchronized with the Operations Control Center

## Data and State Management

The current implementation uses local JSON files for lightweight
persistence.

### Passenger Records

Generated passenger records are stored in:

``` text
mock_data/passengers.json
```

Each PNR is linked to a flight ID. Flight status is derived from the
linked operational flight state.

``` text
PNR → Passenger Record → Flight ID → Operational State
```

### Recovery Records

Applied recovery details are stored in:

``` text
mock_data/recovery_state.json
```

Recovery records can include:

-   Original flight
-   Recovery flight
-   New departure time
-   New gate
-   Seat
-   Voucher information
-   Confirmation status

Resetting a PNR search clears the Passenger Portal view but does not
delete the persisted recovery booking.

## Demo PNR Generator

The Operations page includes a collapsed **Demo Tools** section that
can:

-   Generate a unique six-character PNR
-   Link the passenger to the currently selected flight
-   Store the passenger record
-   Make the generated PNR searchable from the Passenger Portal

## Technology Stack

-   Python
-   Streamlit
-   JSON-based operational and passenger data
-   Streamlit Session State
-   Multi-agent orchestration
-   Custom HTML and CSS

## Project Structure

``` text
airline-disruption/
│
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── 1_Ops_Team.py
│       └── 2_Passenger.py
│
├── mock_data/
│   ├── flights.json
│   ├── passengers.json
│   ├── weather.json
│   └── recovery_state.json
│
├── agents/
│   └── agent implementation files
│
├── bridge/
│   └── orchestration and integration logic
│
├── requirements.txt
└── README.md
```

> Internal agent and bridge filenames may vary by project version.

## Installation and Setup

### 1. Open the project directory

``` powershell
cd C:\Project\airline-disruption
```

### 2. Create a virtual environment

``` powershell
python -m venv .venv
```

### 3. Activate the environment

``` powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

If Streamlit is not included in the requirements file:

``` powershell
python -m pip install streamlit
```

### 5. Run the application

Run from the project root:

``` powershell
python dashboard/api_bridge.py
python -m streamlit run dashboard/app.py
```

## Suggested Demo Flow

1.  Open the Home page and introduce the Operations and Passenger
    experiences.
2.  Enter the Operations Control Center.
3.  Show airport weather conditions and the live flight board.
4.  Select a disrupted flight.
5.  Generate a PNR from Demo Tools.
6.  Run the AI analysis.
7.  Review Weather, Prediction, Recovery, Evaluator, and Communications
    outputs.
8.  Apply the Recovery Plan.
9.  Verify that recovery and communication details reflect the applied
    decision.
10. Open the Passenger Portal.
11. Search the generated PNR.
12. Show the confirmed recovery booking.

## Design Principles

### Shared Operational State

Flight status, disruption analysis, recovery execution, communication,
and passenger recovery use consistent operational facts.

### Specialized Responsibilities

Complex disruption management is divided into focused agent
responsibilities rather than handled as one unrestricted prompt.

### Human-Controlled Execution

A proposed recovery remains a recommendation until the Operations Team
explicitly applies it.

### Communication Based on Applied Decisions

Passenger and staff messages are based on the applied recovery facts to
reduce contradictory information.

### Dynamic Passenger Experience

Passenger results are resolved from the searched PNR and its linked
flight and recovery state rather than from a static passenger scenario.

## Current Scope

The current implementation is a functional prototype using local JSON
persistence and simulated operational data. A production deployment
would typically require:

-   Airline reservation and departure-control system integrations
-   Real-time flight, airport, and weather feeds
-   Durable database storage
-   Authentication and role-based access control
-   Event-driven processing
-   Agent observability and tracing
-   Audit history for operational decisions
-   Email, SMS, and push-notification integrations
-   Retry and failure-handling policies
-   Human approval and operational policy controls

## Future Enhancements

-   Real-time airline and weather APIs
-   Connection-risk-based passenger prioritization
-   Hotel and meal eligibility evaluation
-   Crew legality and duty-time validation
-   Aircraft rotation and gate-conflict analysis
-   Recovery-cost comparison
-   Agent execution timeline and trace visualization
-   Operational KPI dashboard
-   Recovery feedback and evaluation loop
-   Database-backed passenger and recovery management

## Disclaimer

This project uses mock and simulated data and is not connected to a live
airline reservation, operations-control, crew-management, airport, or
passenger-notification system.
