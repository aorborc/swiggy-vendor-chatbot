import subprocess
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_mcp_test():
    # Check for required environment variables
    required_vars = [
        "ACCOUNTS_SERVER_URL", "ANALYTICS_SERVER_URL",
        "ZOHO_CLIENT_ID", "ZOHO_CLIENT_SECRET", "ZOHO_REFRESH_TOKEN"
    ]
    
    env_vars = {}
    missing_vars = []
    for var in required_vars:
        val = os.getenv(var)
        if not val or val.startswith("your_"):
            missing_vars.append(var)
        env_vars[var] = val

    if missing_vars:
        print(f"Error: Missing or default values for required environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with valid credentials.")
        return

    # Construct Docker command
    # Using 'docker run' with -i (interactive) to communicate via stdio
    cmd = [
        "docker", "run",
        "-i", "--rm",
        "-e", f"ACCOUNTS_SERVER_URL={env_vars['ACCOUNTS_SERVER_URL']}",
        "-e", f"ANALYTICS_SERVER_URL={env_vars['ANALYTICS_SERVER_URL']}",
        "-e", f"ANALYTICS_CLIENT_ID={env_vars['ZOHO_CLIENT_ID']}",
        "-e", f"ANALYTICS_CLIENT_SECRET={env_vars['ZOHO_CLIENT_SECRET']}",
        "-e", f"ANALYTICS_REFRESH_TOKEN={env_vars['ZOHO_REFRESH_TOKEN']}",
        # Add other optional vars if needed
        "zohoanalytics/mcp-server:latest"
    ]

    print("Starting Zoho MCP Server via Docker...")
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        text=True,
        bufsize=0 # Unbuffered
    )

    try:
        # 1. Initialize
        print("\n--- Sending Initialize Request ---")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        }
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        # Read response
        response = process.stdout.readline()
        print(f"Received: {response}")
        
        with open("mcp_test_output.log", "w") as f:
            f.write(f"Initialize Response:\n{response}\n\n")
        
        # 2. Initialized Notification
        notify = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        process.stdin.write(json.dumps(notify) + "\n")
        process.stdin.flush()

        # 3. List Tools
        print("\n--- Listing Tools ---")
        list_tools = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        process.stdin.write(json.dumps(list_tools) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print(f"Received: {response}")
        tools_data = json.loads(response)
        
        with open("mcp_test_output.log", "a") as f:
            f.write(f"Tools List Response:\n{json.dumps(tools_data, indent=2)}\n\n")
        
        # Check if export_data tool exists
        tools = tools_data.get("result", {}).get("tools", [])
        
        print(f"\n--- Found {len(tools)} tools ---")
        with open("mcp_test_output.log", "a") as f:
            f.write(f"Total tools found: {len(tools)}\n")
            for tool in tools:
                f.write(f"- {tool.get('name')}\n")
        
        export_tool = next((t for t in tools if t["name"] == "export_data"), None)
        
        if export_tool:
            print("\n--- Found 'export_data' tool ---")
            print(json.dumps(export_tool, indent=2))
            
            # 4. Call Export Data (Example)
            # Note: This requires valid workspace and view names.
            # We will try to call it with placeholder data or ask user to edit this script.
            print("\n--- Attempting to Call 'export_data' ---")
            print("Note: You need to edit this script to provide valid 'workspace_name' and 'view_name'.")
            
            # Uncomment and edit the following block to test actual export
            """
            call_export = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "export_data",
                    "arguments": {
                        "workspace_name": "YOUR_WORKSPACE_NAME",
                        "view_name": "YOUR_VIEW_NAME",
                        "response_format": "JSON"
                    }
                }
            }
            process.stdin.write(json.dumps(call_export) + "\n")
            process.stdin.flush()
            response = process.stdout.readline()
            print(f"Received: {response}")
            """
        else:
            print("\nWarning: 'export_data' tool not found in the list.")
            print("Check mcp_test_output.log for the full list of available tools.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    run_mcp_test()
