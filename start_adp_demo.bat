@echo off
REM One-click startup for ADP demo (Windows)
cd /d %~dp0
start "Auth Server" cmd /k "uvicorn auth_server:app --reload --port 8000"
start "Resource Server" cmd /k "uvicorn resource_server:app --reload --port 8001"
echo Servers starting. Close these windows to stop the servers.
