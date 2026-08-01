# InvoiceIQ — Domain Modeling

## 1. Domain Modeling Goal

The InvoiceIQ domain model represents the business concepts needed to process enterprise vendor invoices.

The first version intentionally focuses on the smallest useful core:

```text
Vendor 1 ──────── * Invoice 1 ──────── * LineItem
```

This model is designed to support invoices with arbitrary numbers of line items and to keep responsibilities separated.

## 2. Core Entity: Vendor

A `Vendor` represents the supplier associated with invoices.

### Attributes

```text
vendor_id
legal_name
tax_id
address
contact_information
```

### Responsibilities

```text
validate_identity()
normalize_details()
```

Vendor owns supplier identity and supplier-specific information.

It should not own invoice-specific data such as invoice date, invoice total, or line items.

## 3. Core Entity: Invoice

An `Invoice` represents one vendor invoice.

### Attributes

```text
invoice_id
invoice_number
invoice_date
due_date
currency
vendor
purchase_order_number
payment_terms
line_items
subtotal
tax_total
discount_total
shipping_total
grand_total
```

### Responsibilities

```text
add_line_item()
calculate_total()
validate()
```

The Invoice owns invoice-level information and the collection of its line items.

## 4. Core Entity: LineItem

A `LineItem` represents one product or service billed on an invoice.

### Attributes

```text
line_number
description
supplier_part_number
quantity
unit_of_measure
unit_price
tax
line_total
```

### Responsibilities

```text
calculate_amount()
validate()
```

A LineItem calculates its own line-level amount.

## 5. Composition

InvoiceIQ uses composition because an invoice contains other domain objects:

```text
Invoice
├── Vendor
└── List[LineItem]
```

This supports:

```text
Invoice A → 2 line items
Invoice B → 15 line items
Invoice C → 250 line items
```

without changing the Invoice class structure.

## 6. Responsibility Matrix

| Concept | Owner | Reason |
|---|---|---|
| Vendor legal name | Vendor | Supplier identity |
| Vendor tax ID | Vendor | Supplier identity |
| Invoice number | Invoice | Identifies invoice |
| Invoice date | Invoice | Applies to whole invoice |
| Due date | Invoice | Applies to whole invoice |
| Currency | Invoice | Applies to invoice financial values |
| PO number | Invoice | Reference associated with invoice |
| Product/service description | LineItem | Describes one billed item |
| Quantity | LineItem | Quantity of one billed item |
| Unit price | LineItem | Price of one billed item |
| Line total | LineItem | Result for one line |
| Subtotal | Invoice | Aggregated invoice-level amount |
| Tax total | Invoice | Invoice-level financial amount |
| Grand total | Invoice | Final invoice amount |
| Add line item | Invoice | Invoice owns line-item collection |
| Calculate line amount | LineItem | LineItem owns quantity and unit price |
| Calculate invoice total | Invoice | Invoice aggregates its lines |

## 7. Class Relationship

```text
┌─────────────────────────┐
│         Vendor          │
├─────────────────────────┤
│ vendor_id               │
│ legal_name              │
│ tax_id                  │
│ address                 │
│ contact_information     │
├─────────────────────────┤
│ validate_identity()     │
│ normalize_details()     │
└────────────┬────────────┘
             │
             │ 1
             │
             │ *
             ▼
┌─────────────────────────┐
│        Invoice          │
├─────────────────────────┤
│ invoice_id              │
│ invoice_number          │
│ invoice_date            │
│ due_date                │
│ currency                │
│ vendor                  │
│ purchase_order_number   │
│ payment_terms           │
│ line_items              │
│ subtotal                │
│ tax_total               │
│ discount_total          │
│ shipping_total          │
│ grand_total             │
├─────────────────────────┤
│ add_line_item()         │
│ calculate_total()       │
│ validate()              │
└────────────┬────────────┘
             │
             │ 1
             │
             │ *
             ▼
┌─────────────────────────┐
│        LineItem         │
├─────────────────────────┤
│ line_number             │
│ description             │
│ supplier_part_number    │
│ quantity                │
│ unit_of_measure         │
│ unit_price              │
│ tax                     │
│ line_total              │
├─────────────────────────┤
│ calculate_amount()      │
│ validate()              │
└─────────────────────────┘
```

## 8. Why Not Put Everything in Invoice?

A poor design would look like:

```text
Invoice
├── vendor_name
├── vendor_address
├── item1_description
├── item1_quantity
├── item1_price
├── item2_description
├── item2_quantity
├── item2_price
└── ...
```

This fails for enterprise invoices because there is no fixed maximum number of line items.

The better design is:

```text
Invoice
├── Vendor
└── List[LineItem]
```

The number of LineItem objects can grow without changing the class definition.

## 9. Why PO and Receipt Are Not Core Classes Yet

Enterprise AP workflows eventually need:

```text
PurchaseOrder
PurchaseOrderLine
ProductReceipt
InvoiceMatchResult
ValidationResult
Exception
Approval
Payment
```

However, these are not all required to implement the first OOP model.

They should be introduced when the corresponding InvoiceIQ capabilities are built.

This prevents premature abstraction and keeps the initial domain model focused.

## 10. Future Enterprise Domain

The domain can eventually evolve into:

```text
Vendor
   │
   │
Invoice ───────── PurchaseOrder
   │                     │
   │                     │
   └────────────── ProductReceipt
                         │
                         ▼
                  Matching Engine
                         │
                 ┌───────┴────────┐
                 ↓                ↓
              Matched          Exception
                 │                │
                 ↓                ↓
             Approval         Human Review
```

This provides the foundation for later:

- Pydantic validation
- SQLAlchemy persistence
- OCR/extraction
- duplicate detection
- 2-way / 3-way matching
- ETL
- ML categorization
- FastAPI services
- analytics
- RAG/search

## 11. Domain Modeling Principle

> Give each object responsibility for the data and behavior that logically belongs to it.

The model should be expanded only when real business requirements justify a new entity or responsibility.
