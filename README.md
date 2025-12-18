# Protected Billing MCP Server

A Model Context Protocol (MCP) server that provides secure access to billing and compute information, integrated with Keycloak for OAuth2 authentication.

## 🚀 Overview

This server exposes tools to fetch compute offerings and VPN user costs. It leverages **FastMCP** for the protocol implementation and **Keycloak** to ensure only authorized users can access sensitive data.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed and configured:

### 1. Python 3.12+ (Recommended) or 3.14+
The project specifies Python 3.14+, but it is compatible with Python 3.12 or higher.
- **Check version:** `python --version`
- **Installation:** Download from [python.org](https://www.python.org/downloads/) or use a version manager like `pyenv`.

### 2. UV Package Manager
This project uses `uv` for lightning-fast dependency management.
- **Installation (Linux/macOS):**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Installation (Windows):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 3. Keycloak Server
You need a running Keycloak instance to handle authentication.
- A **Realm** (e.g., `myrealm`).
- A **Client** for the MCP server (e.g., `mcp-server-client`).
- **Client Protocol**: `openid-connect`.
- **Access Type**: `confidential` (requires a secret).

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mcp-server
```

### 2. Configure Environment Variables
Copy the example environment file and fill in your Keycloak details:
```bash
cp .env.example .env
```
Edit `.env` and set:
- `KEYCLOAK_DOMAIN`: Your Keycloak URL (e.g., `https://auth.example.com`)
- `REALM_NAME`: Your realm name.
- `MCP_SERVER_CLIENT_ID`: The client ID from Keycloak.
- `MCP_SERVER_CLIENT_SECRET`: The client secret from Keycloak.
- `MCP_SERVER_BASE_URL`: The public URL where your MCP server will be accessible (e.g., `http://localhost:8000`).

### 3. Install Dependencies
```bash
uv sync
```

---

## 🏃 Running the Server

To start the MCP server locally:

```bash
uv run app/main.py
```
By default, the server runs on `http://0.0.0.0:8000`.

---

## 📦 Packages Used & Rationale

| Package | Purpose | Why used? |
| :--- | :--- | :--- |
| **fastmcp** | Core Framework | Simplifies MCP server creation with built-in OAuth support and easy tool/resource decorators. |
| **httpx** | HTTP Client | Modern, asynchronous HTTP client for Python, used for making requests to the upstream billing API. |
| **python-dotenv** | Config Management | Loads environment variables from the `.env` file for secure configuration. |
| **python-json-logger** | Structured Logging | Provides logs in JSON format, which is essential for production monitoring and debugging. |
| **pydantic** | Data Validation | Used for defining robust data models (e.g., `TokenClaims`) and validating API responses. |
| **uvicorn** | ASGI Server | Used in `main.py` to serve the HTTP application of FastMCP. |

---

## 🔧 Available Tools

Once connected, the following tools are available to your AI assistant:

1.  **`hello`**: A simple greeting tool that demonstrates extraction of user identity (name/email) from the OAuth token.
2.  **`get_compute_offerings`**: Fetches a list of available compute offerings (PAY_AS_YOU_GO) for the user's zone.
3.  **`get_vpn_user_cost`**: Retrieves the cost associated with VPN users.

---

## 🌐 Deployment

To deploy this MCP server for production:

1.  **Expose the Server**: Use a reverse proxy like **Nginx** or a tunnel like **Cloudflare Tunnel** or **ngrok** to make the server reachable via HTTPS. MCP clients (like Claude) require an HTTPS URL for remote connections.
2.  **Dockerization**: (Optional but recommended)
    ```dockerfile
    FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
    COPY . /app
    WORKDIR /app
    RUN uv sync --frozen
    CMD ["uv", "run", "app/main.py"]
    ```
3.  **Environment Variables**: Ensure all variables in `.env` are set in your production environment.

---

## 🌐 Deployment

The MCP server is currently deployed and accessible at:
**Management URL:** [https://breezy-tomato-rodent.fastmcp.app/mcp](https://breezy-tomato-rodent.fastmcp.app/mcp)
**HTTP Endpoint:** `https://breezy-tomato-rodent.fastmcp.app/mcp`

---

## 🔌 Connecting to AI Clients

Since the server is deployed in the cloud, you can connect to it using the **HTTP** transport. This is the most efficient way to use the protected billing tools.

### 1. Claude Desktop
Add the following to your `claude_desktop_config.json` (typically found at `%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "protected-billing": {
      "url": "https://breezy-tomato-rodent.fastmcp.app/mcp"
    }
  }
}
```

### 2. Claude Code
Run the following command to add the server:
```bash
claude mcp add https://breezy-tomato-rodent.fastmcp.app/mcp
```

### 3. Cursor
1. Open **Cursor Settings** > **Features** > **MCP**.
2. Click **+ Add New MCP Server**.
3. Choose **HTTP**.
4. Set Name: `Billing Server`.
5. Set URL: `https://breezy-tomato-rodent.fastmcp.app/mcp`.

### 4. VS Code Copilot
1. Install an MCP-compatible extension (like "MCP Client").
2. In the extension settings, add the server URL: `https://breezy-tomato-rodent.fastmcp.app/mcp`.

### 5. ChatGPT
1. Use an MCP-to-ChatGPT bridge or a desktop application that supports remote MCP servers.
2. Provide the URL: `https://breezy-tomato-rodent.fastmcp.app/mcp`.

---

## 🛠️ MCP Configuration (mcp.json)

For tools or environments that support an `mcp.json` configuration file, you can use the following definition:

```json
{
  "mcpServers": {
    "billing-service": {
      "type": "http",
      "url": "https://breezy-tomato-rodent.fastmcp.app/mcp"
    }
  }
}
```

---

## 🔥 Testing with MCP Inspector
You can test your server's tools without a full AI client using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector https://breezy-tomato-rodent.fastmcp.app/mcp
```
This will open a web interface where you can trigger tools and see the results.

---

## 🔒 Security Note
This server is protected by OAuth2. Ensure your `MCP_SERVER_CLIENT_SECRET` is never committed to version control and that the server is served over HTTPS in production.
