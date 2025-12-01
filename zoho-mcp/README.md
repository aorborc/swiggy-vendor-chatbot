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

**Note**: The main Swiggy Chatbot application (in `../backend`) now integrates the MCP server directly using the `zoho-analytics-mcp` Python package. It does not require this standalone Docker container to be running.

However, you can still use this directory for:
1.  **Standalone Testing**: Verifying your Zoho credentials and API access independently.
2.  **Development**: Debugging MCP server issues in isolation.

If you are running the full chatbot application, please refer to the root [README.md](../README.md).

Additional integration details:
- The backend reads `VendorPortalReportsList.csv` and turns each row into an MCP export tool with a PAN-aware criteria (default PAN comes from `DEFAULT_VENDOR_PAN` in `backend/.env`).
- Choose your execution mode via `MCP_EXECUTION_MODE` in `backend/.env`: `local` (use the Python package) or `docker` (use this container).

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
