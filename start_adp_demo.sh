#!/bin/bash
# One-click startup for ADP demo (Linux)
cd "$(dirname "$0")"
x-terminal-emulator -e "uvicorn auth_server:app --reload --port 8000" &
x-terminal-emulator -e "uvicorn resource_server:app --reload --port 8001" &
echo "Servers starting in new terminals. Close those terminals to stop the servers."
