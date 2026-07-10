$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$env:PYTHONPATH = $Root
$env:NEURO_SAN_BASE_URL = "http://127.0.0.1:8080"
$env:NEURO_SAN_NETWORK = "airline_disruption"
python dashboard/api_bridge.py
