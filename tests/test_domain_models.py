from invoiceIQ.domain.model import LineItem, Vendor, Invoice

def test_invoice_totals():
    vendor = Vendor(1,"ABC Technologies","GST123","Bengaluru","contact@abc.com")
    
    invoice = Invoice("1","INV-9001","2026-08-01","2026-08-31","INR",vendor,"PO-7821","Net 30",[],0,0,0,0,0)
    
    laptop = LineItem(1,"Laptop",2,"pcs",50000,"LAP123",9000)
    mouse = LineItem(2,"Mouse",5,"pcs",500,"MOU456",450)
    
    invoice.add_line_item(laptop)
    invoice.add_line_item(mouse)

    assert invoice.subtotal == 102500
    assert invoice.tax_total == 9450
    assert invoice.grand_total == 111950