$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
$env:AGENT_MANIFEST_FILE = Join-Path $Root "registries\manifest.hocon"
$env:AGENT_TOOL_PATH = Join-Path $Root "coded_tools"
$env:PYTHONPATH = $Root
Write-Host "Starting Neuro SAN Studio server on port 8080..."
python -m neuro_san_studio run --server-only --server-http-port 8080
