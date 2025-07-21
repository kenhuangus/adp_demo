# Demo AI Agent for ADP
# Simulates an agent registering, requesting delegation, and accessing a resource

import requests

AUTH_SERVER = "http://localhost:8000"

class Agent:
    def __init__(self, agent_name, owner):
        self.agent_name = agent_name
        self.owner = owner
        self.agent_id = None
        self.agent_secret = None
        self.agent_jwt = None
        self.access_token = None

    def register(self):
        print("[STEP] Registering agent...")
        try:
            resp = requests.post(f"{AUTH_SERVER}/register_agent", json={
                "agent_name": self.agent_name,
                "owner": self.owner
            })
            print(f"  [HTTP] Status: {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            self.agent_id = data["agent_id"]
            self.agent_secret = data["agent_secret"]
            self.agent_jwt = data["agent_jwt"]
            print(f"  [OK] Registered agent: {self.agent_id}")
        except Exception as e:
            print(f"  [ERROR] Agent registration failed: {e}")
            raise

    def request_delegation(self, user, scopes):
        print("[STEP] Requesting delegation from user...")
        try:
            resp = requests.post(f"{AUTH_SERVER}/delegate", json={
                "user": user,
                "agent_id": self.agent_id,
                "scopes": scopes
            })
            print(f"  [HTTP] Status: {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            self.delegation_token = data["delegation_token"]
            print(f"  [OK] Obtained delegation token for agent {self.agent_id}")
        except Exception as e:
            print(f"  [ERROR] Delegation request failed: {e}")
            raise

    def get_access_token(self):
        print("[STEP] Exchanging delegation token for access token...")
        try:
            resp = requests.post(f"{AUTH_SERVER}/token", json={
                "agent_id": self.agent_id,
                "agent_secret": self.agent_secret,
                "delegation_token": self.delegation_token
            })
            print(f"  [HTTP] Status: {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            self.access_token = data["access_token"]
            print(f"  [OK] Obtained access token for agent {self.agent_id}")
        except Exception as e:
            print(f"  [ERROR] Access token request failed: {e}")
            raise

    def access_resource(self):
        print("[STEP] Accessing protected resource with access token...")
        resource_url = "http://localhost:8001/calendar"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            resp = requests.get(resource_url, headers=headers)
            print(f"  [HTTP] Status: {resp.status_code}")
            if resp.status_code == 200:
                print("  [OK] Resource server response:", resp.json())
            else:
                print(f"  [ERROR] Resource access failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"  [ERROR] Exception during resource access: {e}")
            raise

if __name__ == "__main__":
    agent = Agent(agent_name="demo-agent", owner="user1")
    agent.register()
    agent.request_delegation(user="user1", scopes=["calendar:read"])  # User must exist in USERS
    agent.get_access_token()
    agent.access_resource()
