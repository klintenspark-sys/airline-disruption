# ✈️ AI-Powered Airline Disruption Management Platform

An interactive multi-agent airline disruption management prototype built
for hackathon demonstration. The platform connects airline operations
analysis, disruption recovery, communication, and passenger self-service
through a shared operational state.

The application provides two coordinated experiences:

-   **Operations Control Center** --- monitor flights, review airport
    weather, analyze disruptions, evaluate recovery options, apply
    recovery plans, and generate synchronized communications.
-   **Passenger Portal** --- search by PNR to view current flight status
    and confirmed recovery details.

## Problem Statement

Airline disruptions such as weather events, ground stops, maintenance
issues, and operational delays require coordination across multiple
teams and systems. This can result in slow decisions, inconsistent
recovery actions, and contradictory communication to passengers and
staff.

This project demonstrates how specialized AI agents can divide the
disruption-management workflow while sharing a consistent operational
and recovery state.

## Solution Overview

The workflow is designed around specialized responsibilities:

1.  **Weather Agent** evaluates weather and environmental conditions
    affecting airport and flight operations.
2.  **Prediction Agent** estimates disruption impact and delay risk.
3.  **Recovery Agent** creates a recovery proposal using flight and
    disruption context.
4.  **Evaluator Agent** reviews the proposed recovery before execution.
5.  **Communications Agent** prepares passenger and staff messages using
    the final operational decision.

The application separates **proposed recovery** from **applied
recovery**. Once the Operations Team applies a plan, the recovery
information is persisted and becomes available to the Passenger Portal
through PNR search.

## Key Features

### Operations Control Center

-   Airport weather status overview
-   Live flight board
-   Flight status filtering
-   Pagination for the flight board
-   On Time, Delayed, and Cancelled flight states
-   Scheduled and estimated timing information
-   Operational stage and current location
-   Automatic affected-airport and disruption-cause selection
-   AI disruption analysis workflow
-   Specialized agent result views
-   Recovery proposal and evaluation
-   Controlled recovery-plan application
-   Updated recovery flight, departure time, gate, passenger, crew, and
    ground-team details
-   Passenger and staff communication synchronized with applied recovery
    state
-   Demo PNR generation for the selected flight

### Passenger Portal

-   PNR-based passenger search
-   Dynamic passenger and flight information
-   Current flight status
-   Confirmed recovery booking details
-   Recovery flight, departure time, gate, and seat information
-   Voucher and notification information where applicable
-   Reset PNR functionality
-   Recovery state synchronized with the Operations Control Center

## End-to-End Demo Flow

``` text
Select a disrupted flight
        ↓
Generate a Demo PNR
        ↓
Run AI Analysis
        ↓
Weather Agent
        ↓
Prediction Agent
        ↓
Recovery Agent
        ↓
Evaluator Agent
        ↓
Communications Agent
        ↓
Apply Recovery Plan
        ↓
Recovery state is persisted
        ↓
Open Passenger Portal
        ↓
Search the generated PNR
        ↓
View confirmed recovery booking
```

## Project Architecture

``` text
                         ┌──────────────────────────┐
                         │      Streamlit UI        │
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
          ┌─────────▼──────────┐              ┌────────▼─────────┐
          │ Operations Control │              │ Passenger Portal │
          │      Center        │              │    PNR Search    │
          └─────────┬──────────┘              └────────┬─────────┘
                    │                                   │
                    ▼                                   │
          ┌────────────────────┐                        │
          │ Multi-Agent Flow   │                        │
          │                    │                        │
          │ Weather            │                        │
          │ Prediction         │                        │
          │ Recovery           │                        │
          │ Evaluator          │                        │
          │ Communications     │                        │
          └─────────┬──────────┘                        │
                    │                                   │
                    ▼                                   ▼
          ┌────────────────────────────────────────────────────┐
          │        Shared Operational & Recovery State         │
          └────────────────────────────────────────────────────┘
```

## Data Model

The prototype uses local JSON files for hackathon-friendly persistence.

### Passenger Records

Dynamically generated demo passengers are stored in:

``` text
mock_data/passengers.json
```

Each passenger PNR is linked to a flight ID. The Passenger Portal
derives the passenger's current flight state through this relationship.

Conceptually:

``` text
PNR
 ↓
Passenger Record
 ↓
Flight ID
 ↓
Operational State
 ↓
On Time / Delayed / Cancelled
```

### Recovery Records

Applied recovery information is stored in:

``` text
mock_data/recovery_state.json
```

The recovery state can include information such as:

-   Original flight
-   Recovery flight
-   New departure time
-   New gate
-   Seat
-   Voucher information
-   Confirmation status

Resetting a PNR search clears the Passenger Portal display state but
does not delete the persisted recovery booking.

## Demo PNR Generator

The Operations page includes a collapsed **Demo Tools** section.

The generator:

-   Creates a unique six-character PNR
-   Links the passenger to the currently selected flight
-   Stores the new passenger record
-   Allows the same PNR to be searched from the Passenger Portal

For the strongest demonstration, generate the demo PNR before applying
the recovery plan.

## Technology Stack

-   **Python**
-   **Streamlit**
-   **JSON-based mock operational data**
-   **Session state for interactive UI behavior**
-   **Multi-agent orchestration layer**
-   **Custom HTML and CSS for dashboard presentation**

## Project Structure

A typical project structure is:

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
│   └── orchestration / integration logic
│
├── requirements.txt
└── README.md
```

> The exact internal agent and bridge filenames may differ depending on
> the project version.

## Getting Started

### 1. Clone or extract the project

Open PowerShell or a terminal and move to the project root:

``` powershell
cd C:\hackathon\airline-disruption
```

### 2. Create a virtual environment

``` powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

``` powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

If Streamlit is not included in the requirements file:

``` powershell
python -m pip install streamlit
```

### 4. Start the application

Run the command from the **project root directory**:

``` powershell
python -m streamlit run dashboard/app.py
```

Streamlit will display the local application address in the terminal.

## Recommended Hackathon Demo

A concise demonstration can follow this sequence:

1.  Open the Home page and introduce the two coordinated user
    experiences.
2.  Enter the Operations Control Center.
3.  Show airport weather and the live flight board.
4.  Select a disrupted flight.
5.  Expand Demo Tools and generate a PNR.
6.  Run AI Analysis.
7.  Walk through Weather, Prediction, Recovery, Evaluator, and
    Communications.
8.  Apply the Recovery Plan.
9.  Show that recovery and communication views now use the applied
    details.
10. Open the Passenger Portal.
11. Search the generated PNR.
12. Show the confirmed recovery booking.

## Design Principles

### Single Operational Source of Truth

Flight board status, disruption analysis, recovery execution,
communication, and passenger recovery should use consistent operational
facts.

### Specialized Agent Responsibilities

The multi-agent design divides a complex workflow into focused
responsibilities instead of asking one prompt to perform every
operational task.

### Human-Controlled Execution

A recovery recommendation is not treated as an executed action. The
Operations Team applies the recovery plan explicitly.

### Communication After Decision

Passenger and staff communication should be generated from the final
applied recovery facts to avoid contradictions.

### Dynamic Passenger Experience

The Passenger Portal resolves information from the searched PNR rather
than displaying one static passenger scenario.

## Current Prototype Scope

This application is a hackathon prototype. Local JSON persistence is
appropriate for controlled demonstration but would be replaced in a
production deployment.

A production implementation could add:

-   Airline reservation and departure-control system integration
-   Real-time flight and airport data feeds
-   Durable relational or document database storage
-   Authentication and role-based access control
-   Message queues and event-driven processing
-   Agent observability and tracing
-   Audit history for recovery decisions
-   Notification delivery through email, SMS, and mobile push
-   Failure handling and agent retry policies
-   Human approval workflows and operational policy constraints

## Future Enhancements

Potential next steps include:

-   Real-time airline and weather APIs
-   Passenger prioritization based on connection risk
-   Automated hotel and meal eligibility evaluation
-   Crew legality and duty-time validation
-   Aircraft rotation and gate-conflict analysis
-   Recovery-cost comparison
-   Agent execution timeline and trace visualization
-   Operational KPI dashboard
-   Recovery acceptance and rejection feedback loop
-   Database-backed PNR and recovery management

## Why Multi-Agent?

Airline disruption management contains several distinct reasoning tasks.
Weather interpretation, delay prediction, recovery planning, policy
evaluation, and communication have different goals and constraints.

The multi-agent approach in this project is intended to:

-   Divide responsibilities clearly
-   Make intermediate decisions visible
-   Allow recovery proposals to be evaluated before execution
-   Keep communication downstream of operational decisions
-   Make the workflow easier to inspect and extend

The value of the architecture is not the number of agents. The value is
the coordinated workflow and consistent state shared across operational
decisions and passenger outcomes.

## Disclaimer

This project is a hackathon prototype using mock and simulated data. It
is not connected to a live airline reservation, operations-control,
crew-management, airport, or passenger-notification system.

## Team

Add your team details here:

``` text
Team Name:
Team Members:
Hackathon:
Project Track:
Contact:
```

## License

Add the appropriate license for your hackathon or organization before
public distribution.
