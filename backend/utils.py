"""Utility functions for the procurement workflow."""
import json
import os
from typing import List, Dict, Optional
from models import Quote, QuoteItem


def load_approved_suppliers() -> List[Dict]:
    """Load approved suppliers from JSON file."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    suppliers_file = os.path.join(data_dir, "approved_suppliers.json")
    
    with open(suppliers_file, 'r') as f:
        data = json.load(f)
        return data.get("suppliers", [])


def find_supplier_by_name(supplier_name: str, suppliers: List[Dict]) -> Optional[Dict]:
    """Find a supplier by name (case-insensitive, partial match)."""
    supplier_name_lower = supplier_name.lower()
    
    # First try exact match
    for supplier in suppliers:
        if supplier["name"].lower() == supplier_name_lower:
            return supplier
    
    # Then try partial match
    for supplier in suppliers:
        if supplier_name_lower in supplier["name"].lower() or supplier["name"].lower() in supplier_name_lower:
            return supplier
    
    return None


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    try:
        import PyPDF2
        import io
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def generate_po_number() -> str:
    """Generate a unique purchase order number."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"PO-{timestamp}"


def format_quote_for_display(quote: Quote) -> str:
    """Format quote information for display."""
    lines = [
        f"**Supplier:** {quote.supplier_name}",
        f"**Quote Number:** {quote.quote_number or 'N/A'}",
        f"**Quote Date:** {quote.quote_date or 'N/A'}",
        "\n**Items:**"
    ]
    
    for item in quote.items:
        lines.append(f"- {item.item_name}: {item.quantity} x ${item.unit_price:.2f} = ${item.total_price:.2f}")
    
    lines.append(f"\n**Total Amount:** ${quote.total_amount:.2f} {quote.currency}")
    
    return "\n".join(lines)
