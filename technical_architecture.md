# Swiggy Vendor Chatbot - Technical Architecture & Deployment Guide

## 1. Executive Summary

The Swiggy Vendor Chatbot is an AI-powered assistant designed to help vendors access their invoice, payment, and account data from Zoho Analytics via a natural language interface. It leverages **Google Gemini** for reasoning and **Zoho Analytics MCP** for real-time data retrieval, wrapped in a modern **React** frontend and **FastAPI** backend.

## 2. System Architecture

### 2.1 High-Level Overview

The system consists of three main components containerized via Docker:

1.  **Frontend (UI)**: A React-based web interface for vendors to chat.
2.  **Backend (API & AI)**: A Python FastAPI service that manages the chat session, communicates with Google Gemini, and executes tools.
3.  **Zoho Integration (MCP)**: A Model Context Protocol (MCP) server (running embedded or as a sidecar) that bridges the AI with Zoho Analytics data.

### 2.2 Component Details

#### **A. Frontend**
*   **Framework**: React 19
*   **Build Tool**: Vite 5
*   **Styling**: Tailwind CSS v3.4
*   **Server**: Nginx (in production Docker image)
*   **Key Features**:
    *   Responsive chat interface.
    *   Markdown rendering for rich text responses (tables, lists).
    *   Real-time communication with the backend.

#### **B. Backend**
*   **Framework**: Python FastAPI
*   **AI Model**: Google Gemini 1.5 Flash
*   **Responsibilities**:
    *   Handling `/chat` API requests.
    *   Managing conversation context.
    *   **Tool Execution**: The backend defines "tools" (functions) that Gemini can call.
    *   **Dynamic Tool Generation**: Reads `VendorPortalReportsList.csv` to dynamically create tools for specific Zoho reports (e.g., `get_invoice_dashboard_2`).

#### **C. Zoho MCP Integration**
*   **Protocol**: Model Context Protocol (MCP)
*   **Implementation**: `zoho-analytics-mcp` Python package.
*   **Functionality**:
    *   Authenticates with Zoho Analytics using OAuth.
    *   Executes SQL-like queries or fetches specific View IDs.
    *   Filters data based on Vendor PAN (Permanent Account Number).
*   **Security**:
    *   Data is filtered by `Vendor PAN` to ensure vendors only see their own data.
    *   OAuth tokens are managed securely via environment variables.

## 3. Deployment Process

The application is designed to be deployed on a Linux server (e.g., Digital Ocean Droplet) using Docker Compose.

### 3.1 Infrastructure Requirements
*   **OS**: Ubuntu 22.04 / 24.04 LTS
*   **Runtime**: Docker Engine & Docker Compose
*   **Hardware**: Basic Droplet (e.g., 1-2 GB RAM is sufficient for this architecture).

### 3.2 Deployment Steps

1.  **Server Preparation**:
    *   SSH into the server.
    *   Run the setup script to install Docker:
        ```bash
        curl -sL https://raw.githubusercontent.com/aorborc/swiggy-vendor-chatbot/main/setup.sh | sudo bash
        ```

2.  **Code Setup**:
    *   Clone the repository:
        ```bash
        git clone https://github.com/aorborc/swiggy-vendor-chatbot.git
        cd swiggy-vendor-chatbot
        ```

3.  **Configuration**:
    *   Create `backend/.env` from `.env.example`.
    *   Populate the following critical secrets:
        *   `GOOGLE_API_KEY`: For Gemini AI.
        *   `ZOHO_CLIENT_ID` & `SECRET`: For Zoho OAuth.
        *   `ZOHO_REFRESH_TOKEN`: For persistent access.
        *   `ZOHO_WORKSPACE_ID`: The target Analytics workspace.

4.  **Launch**:
    *   Run the application stack:
        ```bash
        docker compose up -d --build
        ```
    *   The Frontend is exposed on Port `80`.
    *   The Backend is exposed on Port `8000`.

## 4. Commercials & AI Costs

### 4.1 AI Model: Google Gemini
The system is configured to use **Gemini 1.5 Flash**.

*   **Performance**: "Flash" models are optimized for high speed and low cost, making them ideal for high-volume tasks like chatbots.
*   **Current Status**: Stable.

### 4.2 Estimated Costs (INR)

*Note: Pricing is based on the **Gemini 1.5 Flash** tier. Prices are approximate and subject to exchange rates ($1 USD ≈ ₹84 INR).*

| Item | Unit Cost (USD) | Unit Cost (INR) | Notes |
| :--- | :--- | :--- | :--- |
| **Input (Prompt)** | $0.075 / 1M tokens | **₹6.30 / 1M tokens** | Extremely affordable. 1M tokens is roughly 700,000 words (approx. 20-30 books). |
| **Output (Response)**| $0.30 / 1M tokens | **₹25.20 / 1M tokens** | |
| **Context Caching** | $0.01875 / 1M tokens | **₹1.60 / 1M tokens** | If caching is enabled for large documents. |

**Monthly Projection Example:**
If the chatbot processes **10,000 queries** per month:
*   Avg query (input): 500 tokens
*   Avg response (output): 500 tokens
*   Total Input: 5M tokens = ₹31.50
*   Total Output: 5M tokens = ₹126.00
*   **Total AI Cost**: **~₹160 INR / month** (excluding server costs).

*This makes the AI component negligible in cost compared to server infrastructure.*

### 4.3 Infrastructure Costs (Digital Ocean)
*   **Basic Droplet**: ~$6 - $12 USD / month (**₹500 - ₹1,000 INR / month**).

## 5. Future Roadmap & Scalability
*   **Authentication**: Integrate vendor login to dynamically set the `PAN` instead of using a default/mock.
*   **Caching**: Implement Redis to cache frequent Zoho queries.
*   **Voice**: Add voice-to-text input for accessibility.
