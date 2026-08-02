from pydantic import BaseModel,Field,model_validator



class Vendor(BaseModel):
    vendor_id: int
    legal_name: str
    tax_id: str
    address: str
    contact_information: str


class LineItem(BaseModel):
    line_number: int
    description: str
    quantity: float=Field(gt=0)
    unit_of_measure: str
    unit_price: float=Field(ge=0)
    supplier_part_number: str
    tax: float=Field(ge=0)

   

class Invoice(BaseModel):
    invoice_id: str
    invoice_number: str
    invoice_date: str
    due_date: str
    currency: str
    vendor: Vendor
    purchase_order_number: str
    payment_terms: str
    line_items: list[LineItem]
    subtotal: float
    tax_total: float
    discount_total: float
    shipping_total: float
    grand_total: float

    @model_validator(mode="after")
    def validate_total(self):
        calculated_total=sum(item.quantity * item.unit_price for item in self.line_items) + sum(item.tax for item in self.line_items) - self.discount_total + self.shipping_total
        if self.grand_total != calculated_total:
            raise ValueError(f"Grand total {self.grand_total} does not match calculated total {calculated_total}") 
        return self
