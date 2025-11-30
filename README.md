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

For deploying to a Digital Ocean Ubuntu server, please see our detailed **[Deployment Guide](DEPLOYMENT.md)**.

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

The backend is configured to run the Zoho MCP server automatically. Ensure you have the `zoho-analytics-mcp` package installed (included in `backend/requirements.txt`).


## Environment Variables

### Backend (.env)
- `GEMINI_API_KEY` - Your Google Gemini API key
- `MCP_SERVER_URL` - URL to the Zoho MCP server

### Zoho MCP (.env)
- `ZOHO_CLIENT_ID` - Zoho OAuth client ID
- `ZOHO_CLIENT_SECRET` - Zoho OAuth client secret
- `ZOHO_REFRESH_TOKEN` - Zoho OAuth refresh token
- `ZOHO_ORG_ID` - Your Zoho organization ID

## Usage

1. Start the Zoho MCP server
2. Start the backend server
3. Start the frontend development server
4. Open your browser to the frontend URL
5. Start chatting with the vendor assistant!

## Technologies

- **Backend**: Python, FastAPI, Google Gemini AI
- **Frontend**: React 19, Vite 5, Tailwind CSS v3.4.0, PostCSS
- **Integration**: Zoho Analytics MCP Server
- **Deployment**: Docker, Docker Compose

## License

MIT
