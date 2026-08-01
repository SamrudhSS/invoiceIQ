# InvoiceIQ — Enterprise Invoice Domain Model

## Purpose

InvoiceIQ is designed for large enterprises that process high volumes of vendor invoices every day.

The first domain model focuses on the core business entities required to represent an enterprise invoice:

- `Vendor`
- `Invoice`
- `LineItem`

The model separates invoice-level information from supplier information and individual billed items. This allows invoices with arbitrary numbers of line items to be represented cleanly.

## Core Relationships

```text
Vendor 1 ──────── * Invoice 1 ──────── * LineItem
```

- One `Vendor` can be associated with many `Invoice` records.
- One `Invoice` is associated with one `Vendor`.
- One `Invoice` can contain many `LineItem` records.
- One `LineItem` belongs to one `Invoice`.

## Vendor

Represents the supplier/vendor associated with an invoice.

### Attributes

- `vendor_id` — internal vendor identifier
- `legal_name` — vendor's legal/business name
- `tax_id` — tax identifier such as GSTIN
- `address` — vendor address
- `contact_information` — vendor contact details

### Responsibilities

- `validate_identity()`
- `normalize_details()`

Vendor-specific information should remain separate from invoice-specific information.

## Invoice

The central business entity representing a vendor invoice.

### Attributes

- `invoice_id` — internal application identifier
- `invoice_number` — identifier printed on the invoice
- `invoice_date`
- `due_date`
- `currency`
- `vendor`
- `purchase_order_number`
- `payment_terms`
- `line_items`
- `subtotal`
- `tax_total`
- `discount_total`
- `shipping_total`
- `grand_total`

### Responsibilities

- `add_line_item()`
- `calculate_total()`
- `validate()`

An invoice owns its collection of line items and invoice-level financial totals.

## LineItem

Represents one individual product or service billed on an invoice.

### Attributes

- `line_number`
- `description`
- `supplier_part_number`
- `quantity`
- `unit_of_measure`
- `unit_price`
- `tax`
- `line_total`

### Responsibilities

- `calculate_amount()`
- `validate()`

A line item is responsible for its own amount calculation, while the invoice aggregates the amounts of all line items.

## Responsibility Boundaries

| Information / Behavior | Owner | Reason |
|---|---|---|
| Vendor legal name | `Vendor` | Supplier identity |
| Invoice number | `Invoice` | Identifies the invoice |
| PO number | `Invoice` | Invoice-level business reference |
| Currency | `Invoice` | Currency applicable to the invoice |
| Product/service description | `LineItem` | Describes one billed item |
| Quantity | `LineItem` | Quantity for one billed item |
| Unit price | `LineItem` | Price for one billed item |
| Line amount | `LineItem` | Calculated from quantity and unit price |
| Invoice subtotal | `Invoice` | Aggregates invoice lines |
| Invoice tax total | `Invoice` | Invoice-level financial amount |
| Grand total | `Invoice` | Final invoice-level amount |
| Add a line item | `Invoice` | Invoice owns the line-item collection |
| Calculate one line amount | `LineItem` | LineItem owns its quantity and price |
| Calculate invoice total | `Invoice` | Invoice aggregates its line items |

## Why Composition Is Used

An invoice can contain an arbitrary number of line items. Therefore, the model uses composition:

```text
Invoice
├── Vendor
└── List[LineItem]
```

This avoids a fixed structure such as `item1`, `item2`, `item3`, etc.

## Enterprise Extension Points

The initial model deliberately does not implement every possible enterprise object. Future stages may introduce:

- `PurchaseOrder`
- `PurchaseOrderLine`
- `GoodsReceipt`
- `InvoiceMatchResult`
- `ValidationResult`
- `Exception`
- `Payment`
- `Approval`
- `CostCenter`
- `GLAccount`
- `Category`

These should be added when the corresponding InvoiceIQ capabilities are designed rather than prematurely creating unnecessary classes.

## Dataset and Ground-Truth Strategy

InvoiceIQ should not rely on visual inspection alone to measure extraction quality.

### Initial synthetic dataset

Start with 20–30 synthetic invoices where the ground truth is known exactly.

Synthetic invoices should deliberately vary:

- vendor layouts
- invoice layouts
- number of line items
- missing fields
- multi-page invoices
- tax structures
- discounts
- currencies
- PO and non-PO invoices
- duplicate invoices
- OCR/layout noise

Each generated document should have a corresponding ground-truth representation.

```text
Synthetic Invoice PDF/Image
          |
          +----> Ground Truth JSON
          |
          +----> InvoiceIQ Extraction
                       |
                       v
                Compare Results
                       |
                       v
             Accuracy Metrics
```

### External validation datasets

- **SROIE** — useful for receipt OCR and key-information extraction benchmarking.
- **CORD** — useful for receipt and line-item extraction benchmarking.
- **FUNSD** — useful for general form understanding and document-layout/entity research.

These datasets should be treated as complementary benchmarks rather than as complete representations of enterprise invoices.

## Domain Design Principle

The model follows this rule:

> Give each object responsibility for the data and behavior that logically belongs to it.

This keeps the domain model understandable and provides a clean foundation for later Pydantic models, SQLAlchemy persistence, extraction pipelines, validation, matching, ETL, ML, APIs, analytics, and RAG.

## Day 1 Status

- [x] OOP foundations
- [x] Enterprise invoice domain research
- [x] Vendor model
- [x] Invoice model
- [x] LineItem model
- [x] Relationships defined
- [x] Responsibility boundaries defined
- [x] Ground-truth strategy defined
- [ ] Python implementation
- [ ] Pydantic models
- [ ] SQLAlchemy models
