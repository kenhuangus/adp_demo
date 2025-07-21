# Authorization Server for ADP Demo
# Implements OAuth 2.1 + OpenID Connect extensions for agent registration, delegation, auditing, and revocation

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict, List, Optional
import jwt
import time
import uuid

app = FastAPI()

# In-memory stores for demo
AGENTS = {}
USERS = {"user1": {"password": "demo"}}
DELEGATIONS = {}
AUDIT_LOG = []
REVOKED = set()

SECRET_KEY = "super-secret-key"  # Use env var in prod
ALGORITHM = "HS256"
OAUTH2_SCOPES = ["calendar:read", "calendar:write", "email:send"]

class AgentRegistrationRequest(BaseModel):
    agent_name: str
    owner: str

class AgentRegistrationResponse(BaseModel):
    agent_id: str
    agent_secret: str
    agent_jwt: str

class DelegationRequest(BaseModel):
    user: str
    agent_id: str
    scopes: List[str]

class DelegationTokenResponse(BaseModel):
    delegation_token: str

class TokenRequest(BaseModel):
    agent_id: str
    agent_secret: str
    delegation_token: str

class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

# Agent registration endpoint
@app.post("/register_agent", response_model=AgentRegistrationResponse)
def register_agent(req: AgentRegistrationRequest):
    agent_id = str(uuid.uuid4())
    agent_secret = str(uuid.uuid4())
    agent_jwt = jwt.encode({
        "agent_id": agent_id,
        "agent_name": req.agent_name,
        "owner": req.owner,
        "iat": int(time.time())
    }, SECRET_KEY, algorithm=ALGORITHM)
    AGENTS[agent_id] = {"secret": agent_secret, "owner": req.owner, "jwt": agent_jwt}
    AUDIT_LOG.append({"event": "register_agent", "agent_id": agent_id, "owner": req.owner, "ts": time.time()})
    return {"agent_id": agent_id, "agent_secret": agent_secret, "agent_jwt": agent_jwt}

# User delegates authority to agent
@app.post("/delegate", response_model=DelegationTokenResponse)
def delegate(req: DelegationRequest):
    if req.user not in USERS:
        raise HTTPException(404, "User not found")
    if req.agent_id not in AGENTS:
        raise HTTPException(404, "Agent not found")
    dt = jwt.encode({
        "sub": req.user,
        "agent_id": req.agent_id,
        "scopes": req.scopes,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }, SECRET_KEY, algorithm=ALGORITHM)
    DELEGATIONS[(req.user, req.agent_id)] = dt
    AUDIT_LOG.append({"event": "delegate", "user": req.user, "agent_id": req.agent_id, "scopes": req.scopes, "ts": time.time()})
    return {"delegation_token": dt}

# Agent exchanges delegation token for OAuth access token
@app.post("/token", response_model=OAuthTokenResponse)
def token(req: TokenRequest):
    agent = AGENTS.get(req.agent_id)
    if not agent or agent["secret"] != req.agent_secret:
        raise HTTPException(401, "Invalid agent credentials")
    if req.agent_id in REVOKED:
        raise HTTPException(403, "Agent revoked")
    try:
        dt_payload = jwt.decode(req.delegation_token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(401, "Invalid delegation token")
    if dt_payload["agent_id"] != req.agent_id:
        raise HTTPException(401, "Delegation token does not match agent")
    access_token = jwt.encode({
        "sub": dt_payload["sub"],
        "agent_id": req.agent_id,
        "scopes": dt_payload["scopes"],
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }, SECRET_KEY, algorithm=ALGORITHM)
    AUDIT_LOG.append({"event": "issue_access_token", "agent_id": req.agent_id, "user": dt_payload["sub"], "scopes": dt_payload["scopes"], "ts": time.time()})
    return {"access_token": access_token}

# Auditing endpoint
@app.get("/audit")
def audit():
    return {"audit_log": AUDIT_LOG}

# Revocation endpoint
@app.post("/revoke_agent")
def revoke_agent(agent_id: str):
    if agent_id not in AGENTS:
        raise HTTPException(404, "Agent not found")
    REVOKED.add(agent_id)
    AUDIT_LOG.append({"event": "revoke_agent", "agent_id": agent_id, "ts": time.time()})
    return {"revoked": agent_id}
