import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from tools.zoho import tools_list
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize the model with tools
# TODO: Future Integration - Connect to Zoho MCP Server
# To integrate with the real Zoho MCP server:
# 1. Use an MCP Client to connect to the running Docker container or subprocess.
# 2. Discover tools from the MCP server.
# 3. Register those tools with the Gemini model.
# Example (Conceptual):
# mcp_client = MCPClient(transport="docker", container="zoho-analytics-mcp")
# zoho_tools = mcp_client.get_tools()
# tools_list.extend(zoho_tools)

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-exp',
    tools=tools_list, # Currently using mock tools from tools/zoho.py
    system_instruction="""
    You are a helpful assistant for Swiggy's vendor portal.
    Your goal is to assist vendors with their inquiries regarding invoices, payments, and account statements.
    You have access to tools that can retrieve this information from Zoho Analytics.
    
    When a user asks about invoices, payments, or their account statement, use the appropriate tool to fetch the data.
    Always be polite and professional.
    If you need a vendor ID and it's not provided, ask for it (for this POC, you can assume/suggest 'VENDOR_123' if the user doesn't know).
    Format your responses nicely, using markdown tables for lists of data if appropriate.
    """
)

chat = model.start_chat(enable_automatic_function_calling=True)

class ChatRequest(BaseModel):
    message: str
    vendor_id: Optional[str] = "VENDOR_123"

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Check if API key is set, otherwise return mock response
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key or api_key.startswith("your_"):
             # Simple mock logic for testing without API key
            msg = request.message.lower()
            if "invoice" in msg:
                return ChatResponse(response="Here are your invoices:\n\n| Invoice | Date | Amount | Status |\n|---|---|---|---|\n| INV-001 | 2024-01-15 | $5000.00 | Paid |\n| INV-002 | 2024-02-20 | $7500.50 | Pending |")
            elif "payment" in msg:
                 return ChatResponse(response="You have a payment of $5000.00 on 2024-01-20 for invoice INV-001.")
            elif "statement" in msg:
                 return ChatResponse(response="**Statement of Account**\n\nTotal Billed: $15,700.50\nTotal Paid: $5,000.00\nOutstanding: $10,700.50")
            else:
                return ChatResponse(response="I can help you with invoices, payments, and statements. What would you like to know?")

        response = chat.send_message(request.message)
        return ChatResponse(response=response.text)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        # Fallback mock if real model fails
        return ChatResponse(response=f"I'm currently running in offline mode. (Error: {str(e)})")


@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
