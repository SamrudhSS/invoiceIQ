from pydantic import ValidationError
from invoiceIQ.domain.validation import Vendor, LineItem, Invoice
import pytest

@pytest.fixture
def invoice_test_data():
    vendor_data = {
        "vendor_id": 1,
        "legal_name": "ABC Technologies",
        "tax_id": "GST123",
        "address": "Bengaluru",
        "contact_information": "John Doe, john.doe@abctech.com"
    }
    lineitem1={
            "line_number": 1,
            "description": "Product A",
            "quantity": 5.0,
            "unit_of_measure": "Each",
            "unit_price": 200.0,
            "supplier_part_number": "PART001",
            "tax": 18.0
        }
    lineitem2={
            "line_number": 2,
            "description": "Product B",
            "quantity": 5.0,
            "unit_of_measure": "Each",
            "unit_price": 200.0,
            "supplier_part_number": "PART002",
            "tax": 36.0
        }
    invoice_data = {
        "invoice_id": "1",
        "invoice_number": "INV-9001",
        "invoice_date": "2026-08-01",
        "due_date": "2026-08-31",
        "currency": "INR",
        "vendor": vendor_data,
        "purchase_order_number": "PO-7821",
        "payment_terms": "Net 30",
        "line_items": [lineitem1, lineitem2],
        "subtotal": 2000,
        "tax_total": 54.0,
        "discount_total": 40.0,
        "shipping_total": 600.0,
        "grand_total": 2614.0
    }
    return invoice_data

def test_valid_invoice_validation(invoice_test_data):

    expected_subtotal = sum(item["quantity"] * item["unit_price"] for item in invoice_test_data["line_items"])
    expected_tax_total = sum(item["tax"] for item in invoice_test_data["line_items"])
    expected_grand_total = expected_subtotal + expected_tax_total - invoice_test_data["discount_total"] + invoice_test_data["shipping_total"]

    invoice=Invoice.model_validate(invoice_test_data)
    assert invoice.subtotal == expected_subtotal
    assert invoice.tax_total == expected_tax_total
    assert invoice.grand_total == expected_grand_total

def test_invalid_invoice_validation(invoice_test_data):

    
    invoice_test_data["subtotal"] = 999  # Invalid subtotal
    invoice_test_data["grand_total"] = 9999  # Invalid grand total

    with pytest.raises(ValidationError) :
        Invoice.model_validate(invoice_test_data)
        