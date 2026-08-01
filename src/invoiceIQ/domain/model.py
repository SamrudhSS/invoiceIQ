class LineItem:
    def __init__(self, line_number: int, description: str, quantity: float, unit_of_measure: str,unit_price: float, supplier_part_number: str, tax:float):
        self.line_number = line_number
        self.description = description
        self.quantity = quantity
        self.unit_of_measure = unit_of_measure
        self.unit_price = unit_price
        self.supplier_part_number = supplier_part_number
        self.tax = tax
        

    def calculate_amount(self):
        self.line_total = self.quantity * self.unit_price
        return self.line_total

class Vendor:
    def __init__(self, vendor_id: int, legal_name: str, tax_id: str, address: str, contact_information: str):
        self.vendor_id=vendor_id
        self.legal_name=legal_name
        self.tax_id=tax_id
        self.address=address   
        self.contact_information=contact_information

    def validate_identity(self):
        pass

    def normalize_details(self):
        pass

class Invoice:
    def __init__(self,invoice_id:str,invoice_number:str,invoice_date:str,due_date:str,currency:str,vendor:Vendor,purchase_order_number:str,payment_terms:str,line_items:list[LineItem],subtotal:float,tax_total:float,discount_total:float,shipping_total:float,grand_total:float):
        self.invoice_id=invoice_id
        self.invoice_number=invoice_number
        self.invoice_date=invoice_date
        self.due_date=due_date
        self.currency=currency
        self.vendor=vendor
        self.purchase_order_number=purchase_order_number
        self.payment_terms=payment_terms
        self.line_items=line_items
        self.subtotal=subtotal
        self.tax_total=tax_total
        self.discount_total=discount_total
        self.shipping_total=shipping_total
        self.grand_total=grand_total

    def calculate_totals(self):
        self.subtotal = sum(item.calculate_amount() for item in self.line_items)
        self.tax_total = sum(item.tax for item in self.line_items)  
        self.grand_total = self.subtotal + self.tax_total - self.discount_total + self.shipping_total

    def add_line_item(self, line_item: LineItem):
        self.line_items.append(line_item)
        self.calculate_totals()

if __name__ == "__main__":
    vendor = Vendor(1,"ABC Technologies","GST123","Bengaluru","contact@abc.com")

    invoice = Invoice("1","INV-9001","2026-08-01","2026-08-31","INR",vendor,"PO-7821","Net 30",[],0,0,0,0,0)

    laptop = LineItem(1,"Laptop",2,"pcs",50000,"LAP123",9000)
    mouse = LineItem(2,"Mouse",5,"pcs",500,"MOU456",450)

    invoice.add_line_item(laptop)
    invoice.add_line_item(mouse)

    print(invoice.subtotal)
    print(invoice.grand_total)