#!/usr/bin/env python3
"""
Test script to demonstrate fetching invoice data from Zoho Analytics
using the Invoice Report view via MCP.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mcp_client import zoho_mcp_client
import json

def test_invoice_export():
    """Test exporting invoice data for a vendor."""
    
    print("=" * 60)
    print("Testing Zoho MCP Invoice Export")
    print("=" * 60)
    
    # Check if configured
    if not zoho_mcp_client.is_configured():
        print("\n❌ Zoho MCP is not configured.")
        print("Please set the following environment variables in backend/.env:")
        print("  - ZOHO_WORKSPACE_ID")
        print("  - ZOHO_CLIENT_ID")
        print("  - ZOHO_CLIENT_SECRET")
        print("  - ZOHO_REFRESH_TOKEN")
        return
    
    print("\n✅ Zoho MCP is configured")
    print(f"Workspace ID: {zoho_mcp_client.workspace_id}")
    
    # Test vendor ID (you can change this)
    test_vendor_id = "VENDOR_123"
    
    print(f"\n📊 Fetching invoices for vendor: {test_vendor_id}")
    print("-" * 60)
    
    result = zoho_mcp_client.export_invoice_report(test_vendor_id)
    
    if result:
        print("\n✅ Successfully retrieved data from Zoho MCP")
        print("\nRaw Response:")
        print(json.dumps(result, indent=2))
        
        # Try to parse the content
        if "content" in result:
            try:
                content = result["content"][0]["text"]
                data = json.loads(content)
                
                print(f"\n📈 Total records: {len(data.get('data', []))}")
                
                # Show first few records
                records = data.get("data", [])[:3]
                if records:
                    print("\nSample Records:")
                    for i, record in enumerate(records, 1):
                        print(f"\n  Record {i}:")
                        print(f"    Invoice Number: {record.get('Invoice Number')}")
                        print(f"    Vendor ID: {record.get('Vendor ID')}")
                        print(f"    Vendor Name: {record.get('Vendor Name')}")
                        print(f"    Invoice Amount: {record.get('Invoice Amount')}")
                        print(f"    Payment Status: {record.get('Payment Status')}")
                        print(f"    Due Date: {record.get('Due Date')}")
            except Exception as e:
                print(f"\n❌ Error parsing response: {e}")
    else:
        print("\n❌ No data returned from Zoho MCP")
        print("This could mean:")
        print("  - The vendor ID doesn't exist")
        print("  - There's an authentication issue")
        print("  - The view ID is incorrect")

if __name__ == "__main__":
    test_invoice_export()
