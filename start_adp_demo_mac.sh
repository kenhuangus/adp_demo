#!/bin/bash
# One-click startup for ADP demo (Mac)
cd "$(dirname "$0")"
open -a Terminal "$(pwd)/auth_server.py" --args uvicorn auth_server:app --reload --port 8000 &
open -a Terminal "$(pwd)/resource_server.py" --args uvicorn resource_server:app --reload --port 8001 &
echo "Servers starting in new Terminal windows. Close those windows to stop the servers."
