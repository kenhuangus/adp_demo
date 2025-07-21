# User Web App (CLI for demo)
# Allows user to view agents, delegate, audit, and revoke

import requests
import sys

AUTH_SERVER = "http://localhost:8000"

USER = "user1"


def list_agents():
    print("Agents registered:")
    # For demo, just fetch audit log and filter register_agent events
    resp = requests.get(f"{AUTH_SERVER}/audit")
    for entry in resp.json()["audit_log"]:
        if entry["event"] == "register_agent":
            print(f"  Agent ID: {entry['agent_id']} (owner: {entry['owner']})")

def delegate(agent_id, scopes):
    resp = requests.post(f"{AUTH_SERVER}/delegate", json={
        "user": USER,
        "agent_id": agent_id,
        "scopes": scopes
    })
    print("Delegation token issued:", resp.json()["delegation_token"])

def audit():
    resp = requests.get(f"{AUTH_SERVER}/audit")
    for entry in resp.json()["audit_log"]:
        print(entry)

def revoke(agent_id):
    resp = requests.post(f"{AUTH_SERVER}/revoke_agent", params={"agent_id": agent_id})
    print("Revoked agent:", resp.json()["revoked"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python user_web.py [list|delegate|audit|revoke] ...")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "list":
        list_agents()
    elif cmd == "delegate":
        if len(sys.argv) < 4:
            print("Usage: python user_web.py delegate <agent_id> <scope1,scope2,...>")
            sys.exit(1)
        agent_id = sys.argv[2]
        scopes = sys.argv[3].split(",")
        delegate(agent_id, scopes)
    elif cmd == "audit":
        audit()
    elif cmd == "revoke":
        if len(sys.argv) < 3:
            print("Usage: python user_web.py revoke <agent_id>")
            sys.exit(1)
        agent_id = sys.argv[2]
        revoke(agent_id)
    else:
        print("Unknown command")
