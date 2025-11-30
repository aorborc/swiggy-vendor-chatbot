# Zoho Analytics MCP Server Setup

This directory contains the configuration to run the Zoho Analytics MCP Server using Docker.

## Prerequisites
- Docker and Docker Compose installed.
- A Zoho Analytics account.

## Setup Instructions

1.  **Obtain OAuth Credentials**:
    - Go to [Zoho Developer Console](https://api-console.zoho.com/).
    - Create a new **Self-Client** application.
    - Enable the **Zoho Analytics API** scope.
    - Generate a **Refresh Token**.

2.  **Configure Environment**:
    - Copy `.env.example` to `.env`:
      ```bash
      cp .env.example .env
      ```
    - Edit `.env` and fill in your `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, and `ZOHO_REFRESH_TOKEN`.
    - Ensure `ACCOUNTS_SERVER_URL` and `ANALYTICS_SERVER_URL` match your data center (e.g., `.in` for India, `.com` for US).

3.  **Run the Server**:
    ```bash
    docker-compose up -d
    ```

## Integration
Once running, this MCP server can be connected to your AI agent.
For the Python backend, you would typically use an MCP client to connect to this container (or run the MCP server as a subprocess if not using Docker).
Since we are using Docker, we would connect via an MCP transport (like SSE if supported, or stdio via `docker exec`).

## Testing
To test the connection and API (e.g., `export_data`):
1.  Ensure `.env` is configured with valid credentials.
2.  Run the test script:
    ```bash
    python3 test_mcp_client.py
    ```
    This script will:
    - Start the Docker container.
    - Connect via stdio.
    - List available tools.
    - (Optional) Call `export_data` if you configure the workspace/view names in the script.
