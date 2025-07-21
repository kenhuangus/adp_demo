# Resource Server for ADP Demo
# Protects a resource, validates access tokens issued by auth_server

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import jwt

app = FastAPI()

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

@app.get("/calendar")
def get_calendar(request: Request):
    auth = request.headers.get("authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")
    token = auth[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(401, "Invalid access token")
    if "calendar:read" not in payload.get("scopes", []):
        raise HTTPException(403, "Insufficient scope")
    return {"calendar": ["2025-07-18: Demo meeting", "2025-07-22: NDSS submission"]}
