# Neuro SAN Integration

The live disruption-analysis path is now: Streamlit Ops UI → FastAPI bridge → Neuro SAN server → `airline_disruption` HOCON network → specialist agents → coded tools → final structured result → Streamlit tabs.

## Run order (Windows PowerShell)

1. `python -m pip install -r requirements.txt`
2. Ensure Ollama is running and `llama3.2` is available, or change the HOCON LLM config to your configured provider.
3. Terminal 1: `./start_neuro_san.ps1`
4. Terminal 2: `./start_bridge.ps1`
5. Terminal 3: `./start_dashboard.ps1`
6. Check `http://localhost:8001/health`; `mode` must be `neuro-san-multi-agent` and `neuro_san_reachable` must be `true`.

The bridge deliberately does not fall back to simulated agent output. If Neuro SAN is unavailable, `/analyze` returns HTTP 503 so the demo cannot silently bypass the required framework.
