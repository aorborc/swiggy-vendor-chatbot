# Deployment Guide for Digital Ocean

This guide will help you deploy the Swiggy Vendor Chatbot to a fresh Digital Ocean Ubuntu server.

## Prerequisites

- A Digital Ocean Droplet (Ubuntu 22.04 or 24.04 recommended)
- SSH access to the server
- Your project code pushed to GitHub
- Your `.env` credentials (Gemini API Key, Zoho Credentials)

## Step 1: Initial Server Setup

SSH into your server:
```bash
ssh root@your_server_ip
```

Update system packages:
```bash
apt update && apt upgrade -y
```

## Step 2: Install Docker & Docker Compose

Run the following commands to install Docker:

```bash
# Add Docker's official GPG key:
apt-get install -y ca-certificates curl
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update

# Install Docker packages:
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify installation:
```bash
docker compose version
```

## Step 3: Clone the Repository

```bash
git clone https://github.com/aorborc/swiggy-vendor-chatbot.git
cd swiggy-vendor-chatbot
```

## Step 4: Configure Environment Variables

You need to create the `.env` file for the backend.

```bash
cd backend
cp .env.example .env
nano .env
```

Paste your credentials into the `.env` file:
```ini
GOOGLE_API_KEY=your_gemini_key
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
ZOHO_WORKSPACE_ID=your_workspace_id
ACCOUNTS_SERVER_URL=https://accounts.zoho.in
ANALYTICS_SERVER_URL=https://analyticsapi.zoho.in
```
Save and exit (`Ctrl+X`, `Y`, `Enter`).

Return to the root directory:
```bash
cd ..
```

## Step 5: Deploy

Build and start the containers:

```bash
docker compose up -d --build
```

This will:
1. Build the backend image (installing Python dependencies and Zoho MCP).
2. Build the frontend image (building React app and setting up Nginx).
3. Start both services.

## Step 6: Verify Deployment

Check if containers are running:
```bash
docker compose ps
```

You should see `chatbot-backend` and `chatbot-frontend` running.

Access your application by visiting your server's IP address in a browser:
`http://your_server_ip`

## Troubleshooting

View logs:
```bash
docker compose logs -f
```

Restart services:
```bash
docker compose restart
```

Update application (after pushing changes to GitHub):
```bash
git pull
docker compose up -d --build
```
