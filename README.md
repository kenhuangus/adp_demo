# Agent Delegation Protocol (ADP) Demo

## 1. What is this project about?
This project demonstrates the **Agent Delegation Protocol (ADP)**, a secure, standards-based framework for delegating authority from humans to AI agents. ADP extends OAuth 2.1 and OpenID Connect with agent registration, delegation tokens, auditable trust chains, and revocation, enabling users to safely empower AI agents to act on their behalf.

## 2. Why ADP?
As AI agents become more autonomous and integrated into business workflows, users need a secure, auditable way to grant agents limited authority over sensitive resources (like calendars, email, or files). ADP addresses this need by:
- Building on widely adopted standards (OAuth 2.1, OpenID Connect)
- Providing explicit, auditable delegation and revocation
- Ensuring accountability and limiting agent privileges
- Enabling safe adoption of AI agents in regulated and sensitive environments

## 3. Startup Scripts
To make it easy to launch the demo, one-click startup scripts are provided for all major platforms:

- **Windows:** `start_adp_demo.bat`  
  Opens two terminals: one for the Authorization Server (port 8000), one for the Resource Server (port 8001).
  
  Usage (in PowerShell or CMD):
  ```
  .\start_adp_demo.bat
  ```

- **Linux:** `start_adp_demo.sh`  
  Launches both servers in new terminal windows (may require `x-terminal-emulator` or similar).
  
  Usage:
  ```
  bash start_adp_demo.sh
  ```

- **Mac:** `start_adp_demo_mac.sh`  
  Launches both servers in new Terminal windows.
  
  Usage:
  ```
  bash start_adp_demo_mac.sh
  ```

## 4. What happens when you run `agent.py`?
Running `python agent.py` executes a full ADP delegation flow:
1. **Agent Registration:** The agent registers with the Authorization Server.
2. **Delegation Request:** The agent requests delegated authority from the user for specific scopes.
3. **Delegation Token Issued:** The server issues a signed delegation token (JWT).
4. **Access Token Exchange:** The agent exchanges the delegation token for an OAuth2 access token.
5. **Resource Access:** The agent uses the access token to access the protected resource server (`/calendar`).
6. **Output:** Step-by-step logs and the resource server’s response are printed in your terminal.

## 5. How is this demo implemented?
- **Backend:** Python (FastAPI) for both Authorization Server and Resource Server
- **Agent:** Python script simulating an AI agent
- **User CLI:** `user_web.py` script for audit and revocation actions
- **Tokens:** JWT (pyjwt) for delegation and access tokens
- **Standards:** OAuth 2.1 and OpenID Connect flows extended for agent delegation
- **Audit:** All actions are logged and viewable at `http://localhost:8000/audit`

## 6. How to contribute
Contributions are welcome! To get started:
- Fork this repo and clone it locally
- Install dependencies: `pip install -r requirements.txt`
- Use the startup scripts to launch the servers
- Add new features, improve documentation, or suggest enhancements via pull requests
- For major changes, please open an issue first to discuss your ideas

## 7. License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
