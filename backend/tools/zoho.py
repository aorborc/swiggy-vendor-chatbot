import json
from typing import List, Dict, Any
from tools.mcp_client import zoho_mcp_client

def get_vendor_invoices(vendor_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves a list of invoices for a specific vendor.
    Tries to fetch from real Zoho Analytics first, falls back to mock data.
    """
    # Try real data first using export_view
    if zoho_mcp_client.is_configured():
        result = zoho_mcp_client.export_invoice_report(vendor_id)
        if result and "content" in result:
            try:
                content = result["content"][0]["text"]
                # Parse the exported JSON data
                data = json.loads(content)
                
                # Filter for the specific vendor
                invoices = []
                for row in data.get("data", []):
                    if row.get("Vendor ID") == vendor_id or row.get("Vendor Code") == vendor_id:
                        invoices.append({
                            "invoice_number": row.get("Invoice Number"),
                            "date": row.get("Invoice Date"),
                            "amount": row.get("Invoice Amount", row.get("Invoice Value")),
                            "status": row.get("Payment Status"),
                            "due_date": row.get("Due Date"),
                            "outstanding": row.get("Outstanding payment", row.get("Total Pending Payment"))
                        })
                
                if invoices:
                    return invoices[:10]  # Limit to 10 invoices
            except Exception as e:
                print(f"Error parsing MCP response: {e}")
    
    # Fall back to mock data
    print("Using mock invoice data")
    invoices = [
        {"invoice_number": "INV-001", "date": "2024-01-15", "amount": 5000.00, "status": "Paid"},
        {"invoice_number": "INV-002", "date": "2024-02-20", "amount": 7500.50, "status": "Pending"},
        {"invoice_number": "INV-003", "date": "2024-03-10", "amount": 3200.00, "status": "Overdue"},
    ]
    return invoices

def get_vendor_payments(vendor_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves payment history for a specific vendor.
    """
    # Try real data first
    if zoho_mcp_client.is_configured():
        sql_query = f"""
        SELECT payment_id, date, amount, invoice_ref, method 
        FROM Payments 
        WHERE vendor_id = '{vendor_id}'
        LIMIT 10
        """
        result = zoho_mcp_client.query_data(sql_query)
        if result and "content" in result:
            try:
                content = result["content"][0]["text"]
                rows = json.loads(content)
                if len(rows) > 1:
                    headers = rows[0]
                    data_rows = rows[1:]
                    payments = []
                    for row in data_rows:
                        payment = dict(zip(headers, row))
                        payments.append(payment)
                    return payments
            except Exception as e:
                print(f"Error parsing MCP response: {e}")
    
    # Fall back to mock data
    print("Using mock payment data")
    payments = [
        {"payment_id": "PAY-101", "date": "2024-01-20", "amount": 5000.00, "invoice_ref": "INV-001", "method": "Bank Transfer"},
    ]
    return payments

def get_statement_of_account(vendor_id: str) -> Dict[str, Any]:
    """
    Generates a statement of account summary for a vendor.
    """
    # Try real data first
    if zoho_mcp_client.is_configured():
        sql_query = f"""
        SELECT 
            SUM(total_amount) as total_billed,
            SUM(paid_amount) as total_paid,
            SUM(total_amount - paid_amount) as outstanding_balance
        FROM Invoices 
        WHERE vendor_id = '{vendor_id}'
        """
        result = zoho_mcp_client.query_data(sql_query)
        if result and "content" in result:
            try:
                content = result["content"][0]["text"]
                rows = json.loads(content)
                if len(rows) > 1:
                    data = rows[1][0]  # First data row
                    return {
                        "vendor_id": vendor_id,
                        "total_billed": data[0] or 0,
                        "total_paid": data[1] or 0,
                        "outstanding_balance": data[2] or 0,
                        "currency": "INR",
                        "generated_at": "2024-03-25"
                    }
            except Exception as e:
                print(f"Error parsing MCP response: {e}")
    
    # Fall back to mock data
    print("Using mock SOA data")
    soa = {
        "vendor_id": vendor_id,
        "total_billed": 15700.50,
        "total_paid": 5000.00,
        "outstanding_balance": 10700.50,
        "currency": "INR",
        "generated_at": "2024-03-25"
    }
    return soa

tools_list = [get_vendor_invoices, get_vendor_payments, get_statement_of_account]
