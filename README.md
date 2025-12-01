# Swiggy Vendor Chatbot POC

A proof-of-concept chatbot for Swiggy vendors that integrates with Zoho Analytics to provide intelligent responses about invoices and vendor data.

## Project Structure

```
chatbot/
├── backend/          # Python FastAPI backend with Gemini AI integration
├── frontend/         # React + Vite frontend with modern UI
└── zoho-mcp/        # Zoho Analytics MCP server integration
```

## Features

- 🤖 AI-powered chatbot using Google Gemini
- 📊 Real-time data from Zoho Analytics
- 💬 Modern, responsive chat interface
- 🔄 Hybrid approach combining AI with real vendor data
- 🐳 Docker support for easy deployment

## Quick Start (Docker Compose)

The easiest way to run the application is using Docker Compose.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/aorborc/swiggy-vendor-chatbot.git
    cd swiggy-vendor-chatbot
    ```

2.  **Configure Environment**:
    ```bash
    cd backend
    cp .env.example .env
    # Edit .env with your Google Gemini and Zoho credentials
    cd ..
    ```

3.  **Run with Docker Compose**:
    ```bash
    docker compose up -d --build
    ```

4.  **Access the App**:
    - Frontend: `http://localhost:80`
    - Backend: `http://localhost:8000`

## Deployment

For a fresh Digital Ocean Ubuntu server:

1.  **SSH into your server**:
    ```bash
    ssh root@your_server_ip
    ```

2.  **Run the Setup Script** (installs Docker & dependencies):
    ```bash
    curl -sL https://raw.githubusercontent.com/aorborc/swiggy-vendor-chatbot/main/setup.sh | sudo bash
    ```

3.  **Clone the Repository**:
    ```bash
    git clone https://github.com/aorborc/swiggy-vendor-chatbot.git
    cd swiggy-vendor-chatbot
    ```

4.  **Configure Secrets**:
    ```bash
    cd backend
    cp .env.example .env
    nano .env
    # Paste your API keys and save (Ctrl+X, Y, Enter)
    cd ..
    ```

5.  **Launch**:
    ```bash
    docker compose up -d --build
    ```

For more details, see the full **[Deployment Guide](DEPLOYMENT.md)**.

## Local Development (Manual Setup)

If you prefer to run services locally without Docker:

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

**Important Notes**: 
- The frontend is configured to connect to the backend at `http://localhost:8000`. Make sure the backend is running before starting the frontend.
- This project uses **Tailwind CSS v3.4.0** with PostCSS. The `postcss.config.js` file is required for Tailwind to work properly.

### 3. Zoho MCP Server

The backend calls Zoho Analytics through the `zoho-analytics-mcp` Python package. With `MCP_EXECUTION_MODE=local` (default) no extra container is required. Set `MCP_EXECUTION_MODE=docker` if you prefer to run the Zoho MCP server image instead.


## Environment Variables

Edit `backend/.env` (see `.env.example` for defaults):
- `GOOGLE_API_KEY` - Google Gemini API key
- `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, `ZOHO_REFRESH_TOKEN`, `ZOHO_WORKSPACE_ID` - Zoho OAuth + workspace
- `ACCOUNTS_SERVER_URL`, `ANALYTICS_SERVER_URL` - Zoho endpoints (match your data center)
- `MCP_EXECUTION_MODE` - `local` (use installed package) or `docker` (run `zohoanalytics/mcp-server`)
- `DEFAULT_VENDOR_PAN` - Fallback PAN when user PAN is missing (demo default: `AAMCA0969R`)
- `ZOHO_EXPORT_DIR` - Directory for MCP export files (default: system temp)

## Usage

1. Ensure Zoho credentials are set; start the Zoho MCP server only if using `MCP_EXECUTION_MODE=docker` (skip for `local`).
2. Start the backend server.
3. Start the frontend development server.
4. Open your browser to the frontend URL.
5. Start chatting with the vendor assistant. PAN is taken from the user login; otherwise `DEFAULT_VENDOR_PAN` is used.

**Report catalog & PAN handling**
- Report definitions are read from `VendorPortalReportsList.csv` at startup; each row becomes a tool (e.g., `get_invoice_dashboard_2`) with its view ID and PAN criteria.
- Slugs (Report Number order): `za_monthly_summary`, `yearly_summary`, `invoice_dashboard_1`, `invoice_dashboard_2`, `payment_report_1`, `payment_report_2`, `payment_adjustment_at_invoice_level`, `debit_note_dashboard_1`, `debit_note_dashboard_2`, `ar_invoice_report_1`, `ar_invoice_report_2`, `private_url_testing`, `collection_adjustment_at_ar_invoice_level`.
- Default PAN: `DEFAULT_VENDOR_PAN` (demo: `AAMCA0969R`).

You can exercise a specific report directly:
```bash
cd backend
python3 - <<'PY'
from tools.zoho_service import zoho_service
print(zoho_service.fetch_report("invoice_dashboard_2", pan="AAMCA0969R"))
PY
```
Requires valid Zoho credentials; otherwise returns `None`.

**Testing**
- Criteria/test coverage without live Zoho: `cd backend && python3 -m unittest test_zoho_reports.py`
- Backend health once running: `curl http://localhost:8000/health`

## Technologies

- **Backend**: Python, FastAPI, Google Gemini AI
- **Frontend**: React 19, Vite 5, Tailwind CSS v3.4.0, PostCSS
- **Integration**: Zoho Analytics MCP Server
- **Deployment**: Docker, Docker Compose

## License

MIT
