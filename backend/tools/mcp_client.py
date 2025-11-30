import subprocess
import json
import os
from typing import Optional, Dict, Any

class ZohoMCPClient:
    """
    A client to interact with the Zoho Analytics MCP server via Docker.
    This provides a hybrid approach where we can call real Zoho tools when needed.
    """
    
    def __init__(self):
        self.accounts_url = os.getenv("ACCOUNTS_SERVER_URL", "https://accounts.zoho.in")
        self.analytics_url = os.getenv("ANALYTICS_SERVER_URL", "https://analyticsapi.zoho.in")
        self.client_id = os.getenv("ZOHO_CLIENT_ID")
        self.client_secret = os.getenv("ZOHO_CLIENT_SECRET")
        self.refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")
        self.workspace_id = os.getenv("ZOHO_WORKSPACE_ID")
        
    def is_configured(self) -> bool:
        """Check if all required credentials are configured."""
        if not all([self.client_id, self.client_secret, self.refresh_token, self.workspace_id]):
            return False
        return all([
            not self.client_id.startswith("your_"),
            not self.client_secret.startswith("your_"),
            not self.refresh_token.startswith("your_"),
            not self.workspace_id.startswith("your_")
        ])
    
    
    def export_invoice_report(self, vendor_id: str) -> Optional[Dict[str, Any]]:
        """
        Export invoice data from the Invoice Report view for a specific vendor.
        Returns the invoice data or None if not configured.
        """
        if not self.is_configured():
            print("Zoho MCP not configured, using mock data")
            return None
            
        try:
            # Construct Docker command
            # Determine execution mode
            execution_mode = os.getenv("MCP_EXECUTION_MODE", "docker")
            
            if execution_mode == "local":
                # Run directly as a command (installed via pip)
                cmd = ["zoho-analytics-mcp"]
                # Pass environment variables to the subprocess
                env = os.environ.copy()
                env.update({
                    "ACCOUNTS_SERVER_URL": self.accounts_url,
                    "ANALYTICS_SERVER_URL": self.analytics_url,
                    "ANALYTICS_CLIENT_ID": self.client_id,
                    "ANALYTICS_CLIENT_SECRET": self.client_secret,
                    "ANALYTICS_REFRESH_TOKEN": self.refresh_token,
                })
            else:
                # Default: Run via Docker
                cmd = [
                    "docker", "run", "-i", "--rm",
                    "-e", f"ACCOUNTS_SERVER_URL={self.accounts_url}",
                    "-e", f"ANALYTICS_SERVER_URL={self.analytics_url}",
                    "-e", f"ANALYTICS_CLIENT_ID={self.client_id}",
                    "-e", f"ANALYTICS_CLIENT_SECRET={self.client_secret}",
                    "-e", f"ANALYTICS_REFRESH_TOKEN={self.refresh_token}",
                    "zohoanalytics/mcp-server:latest"
                ]
                env = None

            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,
                env=env
            )
            
            # Initialize
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "swiggy-chatbot", "version": "1.0"}
                }
            }
            process.stdin.write(json.dumps(init_request) + "\n")
            process.stdin.flush()
            response = process.stdout.readline()
            
            # Send initialized notification
            notify = {"jsonrpc": "2.0", "method": "notifications/initialized"}
            process.stdin.write(json.dumps(notify) + "\n")
            process.stdin.flush()
            
            # Call export_view tool to get invoice data
            call_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "export_view",
                    "arguments": {
                        "workspace_id": self.workspace_id,
                        "view_id": "234338000004384036",  # Invoice Report view ID
                        "response_file_format": "json",
                        "response_file_path": "/tmp/invoice_export.json"
                    }
                }
            }
            process.stdin.write(json.dumps(call_request) + "\n")
            process.stdin.flush()
            
            response = process.stdout.readline()
            process.terminate()
            
            result = json.loads(response)
            if "result" in result:
                return result["result"]
            return None
            
        except Exception as e:
            print(f"Error calling Zoho MCP: {e}")
            return None

# Singleton instance
zoho_mcp_client = ZohoMCPClient()
