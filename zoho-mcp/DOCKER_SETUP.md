# Docker Installation and Zoho MCP Setup Guide (macOS)

## Step 1: Install Docker

You have several options for installing Docker on macOS:

### Option A: Docker Desktop (Recommended for beginners)

1. **Download Docker Desktop**:
   - Visit: https://docs.docker.com/desktop/setup/install/mac-install/
   - Download the appropriate version for your Mac:
     - **Apple Silicon (M1/M2/M3)**: Download "Mac with Apple chip"
     - **Intel Mac**: Download "Mac with Intel chip"

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file
   - Drag Docker.app to your Applications folder
   - Open Docker from Applications
   - Follow the setup wizard
   - Accept the terms and conditions

3. **Verify Installation**:
   ```bash
   docker --version
   docker ps
   ```
   You should see the Docker version and an empty list of containers.

### Option B: Colima (Lightweight alternative)

If you prefer a lightweight, open-source alternative:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Colima and Docker CLI
brew install colima docker

# Start Colima
colima start

# Verify
docker --version
docker ps
```

## Step 2: Pull the Zoho MCP Server Image

Once Docker is running:

```bash
docker pull zohoanalytics/mcp-server:latest
```

This will download the official Zoho Analytics MCP server image.

## Step 3: Verify Your Environment

Navigate to the zoho-mcp directory and check your `.env` file:

```bash
cd /Users/ruben/Projects/Swiggy/chatbot/zoho-mcp
cat .env
```

Ensure these variables are set correctly:
- `ACCOUNTS_SERVER_URL` (e.g., https://accounts.zoho.in)
- `ANALYTICS_SERVER_URL` (e.g., https://analyticsapi.zoho.in)
- `ZOHO_CLIENT_ID`
- `ZOHO_CLIENT_SECRET`
- `ZOHO_REFRESH_TOKEN`

## Step 4: Run the Test Script

```bash
cd /Users/ruben/Projects/Swiggy/chatbot/zoho-mcp
source venv/bin/activate
python test_mcp_client.py
```

## Expected Output

If everything is configured correctly, you should see:

```
Starting Zoho MCP Server via Docker...

--- Sending Initialize Request ---
Received: {"jsonrpc":"2.0","id":1,"result":{...}}

--- Listing Tools ---
Received: {"jsonrpc":"2.0","id":2,"result":{"tools":[...]}}

--- Found 'export_data' tool ---
{
  "name": "export_data",
  "description": "...",
  "inputSchema": {...}
}
```

## Troubleshooting

### Docker daemon not running
**Error**: `Cannot connect to the Docker daemon`
**Solution**: 
- For Docker Desktop: Open Docker Desktop app from Applications
- For Colima: Run `colima start`

### Permission denied
**Error**: `permission denied while trying to connect to the Docker daemon socket`
**Solution**: 
```bash
sudo chmod 666 /var/run/docker.sock
```

### Image pull fails
**Error**: `Error response from daemon: Get "https://registry-1.docker.io/v2/": ...`
**Solution**: Check your internet connection and try again

### Invalid credentials
**Error**: Authentication errors from Zoho
**Solution**: 
1. Verify your credentials at https://api-console.zoho.com/
2. Ensure your refresh token hasn't expired
3. Check that the data center URLs match your account region

## Next Steps

Once the test succeeds:
1. You can integrate the MCP client into the main backend
2. Replace the mock tools with real Zoho MCP tools
3. Test the chatbot with live Zoho Analytics data
