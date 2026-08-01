# InvoiceIQ — Enterprise Research

## 1. Project Goal

InvoiceIQ is intended for large enterprises that receive and process high volumes of vendor invoices every day.

The goal is not merely to extract text from an invoice. The system should help Accounts Payable (AP) teams move from document ingestion to structured data, validation, matching, exception handling, and downstream processing.

A useful enterprise pipeline is:

```text
Invoice arrives
      ↓
Document ingestion
      ↓
OCR / document understanding
      ↓
Field + line-item extraction
      ↓
Structured invoice
      ↓
Validation
      ↓
Duplicate / anomaly checks
      ↓
PO / receipt matching
      ↓
      ┌───────────────┐
      │               │
      ↓               ↓
  Valid invoice    Exception
      ↓               ↓
 Approval / post   Human review
      ↓
 Analytics / search / ERP integration
```

## 2. What Real Enterprise Systems Tell Us

### Microsoft Dynamics 365

Microsoft describes vendor invoices as requests for payment for products or services. Vendor invoices can be based on purchase orders, but they can also be non-PO invoices such as ongoing service bills.

A vendor invoice contains a header and one or more lines for products or services. Microsoft also documents the relationship between purchase orders, product receipts, and vendor invoices.

Important implications for InvoiceIQ:

- PO-based and non-PO invoices must both be supported.
- An invoice can contain multiple lines.
- Product receipt quantities can be relevant to invoice quantities.
- Invoice matching can happen at line level or total level.
- Invoice workflows and approval are part of enterprise AP processing.
- High-volume processing and automation matter.

Source: Microsoft Learn — Vendor invoices overview.

## 3. Invoice Structure

SAP documents invoices as having two broad sections:

### Header-level information

Header fields apply to the entire invoice. Depending on configuration, they can include:

- invoice summary
- tax
- shipping
- order information
- discount
- special handling
- payment terms
- comments
- attachments
- pricing details

### Line-level information

Line fields describe individual billed items or services. Depending on configuration, these can include:

- line number
- description
- item/product information
- quantity
- unit of measure
- unit price
- amount
- tax
- discount
- special handling
- service information

Therefore InvoiceIQ must distinguish between **invoice-level fields** and **line-level fields**.

Source: SAP Help Portal — Invoice Header and Line Item Fields.

## 4. Enterprise Invoice Fields for the Initial Model

### Vendor / supplier

- internal vendor ID
- legal name
- tax ID
- address
- contact/payment information

### Invoice header

- internal invoice ID
- invoice number
- invoice date
- due date
- currency
- purchase order reference
- payment terms
- buyer/legal entity information where available

### Line item

- line number
- description
- supplier part/item number
- quantity
- unit of measure
- unit price
- tax
- line total

### Financial summary

- subtotal
- discount
- shipping/charges
- tax total
- grand total

### Processing metadata

These are not necessarily printed on the source invoice, but are important to InvoiceIQ as a processing platform:

- extraction confidence
- validation status
- duplicate status
- matching status
- processing status
- exception status

## 5. Why Enterprises Need More Than OCR

Extraction is only the first step.

### Validation

InvoiceIQ should eventually verify things such as:

- required fields are present
- totals are mathematically consistent
- tax values are plausible
- line totals agree with quantity × unit price
- invoice dates are valid
- vendor identity can be resolved

### Duplicate detection

Large enterprises may receive repeated or re-submitted invoices. InvoiceIQ should eventually detect likely duplicates using combinations of:

- vendor
- invoice number
- amount
- invoice date
- PO/reference
- extracted document fingerprints

### PO matching

A PO provides an expected purchasing context. InvoiceIQ should eventually compare invoice information against the associated PO.

### Three-way matching

Enterprise AP systems commonly compare:

```text
Purchase Order
      ↕
Invoice
      ↕
Product Receipt
```

Microsoft documents two-way and three-way matching. Two-way matching compares invoice and PO information such as unit price. Three-way matching additionally compares invoice quantities with matched product-receipt quantities.

### Exception handling

A discrepancy should not simply make the system fail.

Examples:

```text
Invoice quantity > received quantity
Invoice unit price ≠ PO unit price
Invoice total ≠ calculated total
PO reference missing
Vendor cannot be confidently identified
Duplicate suspected
```

These should become structured exceptions that can be reviewed by an AP user.

## 6. What This Means for InvoiceIQ

The project should be designed around these enterprise outcomes:

1. Reduce manual invoice data entry.
2. Extract structured invoice and line-item data.
3. Preserve confidence and provenance for extracted values.
4. Validate financial consistency.
5. Identify duplicates and suspicious invoices.
6. Support PO and non-PO invoices.
7. Support two-way and three-way matching.
8. Route discrepancies to human review.
9. Process many invoices efficiently.
10. Produce data usable by analytics and downstream ERP/accounting systems.

## 7. Dataset Strategy

### Synthetic invoices — first

Start with approximately 20–30 synthetic invoices.

Generate documents with controlled ground truth so every extracted field can be compared against the known correct value.

The initial dataset should include:

- different vendor layouts
- different invoice layouts
- one-page and multi-page invoices
- varying line counts
- missing fields
- different tax structures
- discounts
- shipping/charges
- multiple currencies
- PO invoices
- non-PO invoices
- duplicate invoices
- OCR/layout noise

Recommended structure:

```text
datasets/
└── synthetic/
    ├── invoices/
    │   ├── invoice_001.pdf
    │   ├── invoice_002.pdf
    │   └── ...
    └── ground_truth/
        ├── invoice_001.json
        ├── invoice_002.json
        └── ...
```

### SROIE

SROIE is useful for receipt OCR and key-information extraction benchmarking. It should not be treated as a complete enterprise-invoice dataset because it focuses on scanned receipts.

Use it for:

- OCR evaluation
- basic key-information extraction
- robustness against scanned documents

### CORD

CORD is a receipt parsing dataset with OCR boxes/text and semantic labels. It is useful for studying post-OCR parsing and line-item-like receipt structures.

Use it for:

- OCR/post-OCR parsing
- receipt field extraction
- structured line-level parsing research

### FUNSD

FUNSD is useful for general form understanding, semantic entity recognition, and relationships/layout research.

Use it if InvoiceIQ later explores:

- layout-aware models
- document entity relationships
- form understanding

## 8. Ground-Truth Evaluation

The synthetic dataset gives us exact expected values.

The evaluation process should be:

```text
Source Invoice
      ↓
InvoiceIQ extraction
      ↓
Predicted structured data
      ↓
Compare with ground truth
      ↓
Field-level metrics
```

Potential metrics:

- exact match
- precision
- recall
- F1
- numeric error/tolerance
- line-item detection accuracy
- document-level success rate

This is much stronger than manually looking at a few extracted invoices and deciding that they "look correct."

## 9. Important Design Conclusion

The core domain should begin with:

```text
Vendor 1 ──────── * Invoice 1 ──────── * LineItem
```

But the enterprise workflow eventually extends toward:

```text
Vendor
   │
Invoice ───── PurchaseOrder
   │               │
   │               │
   └─────── ProductReceipt
              ↓
       Matching / Validation
              ↓
         Exception handling
              ↓
       Approval / Processing
```

The architecture should grow from researched business requirements rather than from arbitrary classes.

## References

- Microsoft Learn — Vendor invoices overview:
  https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/vendor-invoices-overview

- Microsoft Learn — Accounts payable invoice matching validation:
  https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/tasks/set-up-accounts-payable-invoice-matching-validation

- Microsoft Learn — Purchase order overview:
  https://learn.microsoft.com/en-us/dynamics365/supply-chain/procurement/purchase-order-overview

- SAP Help Portal — Invoice Header and Line Item Fields:
  https://help.sap.com/docs/business-network-for-trading-partners/creating-and-managing-invoices-credit-memos-and-debit-memos/invoice-header-and-line-item-fields-dd2419d1f018101490228b444c92b07f

- CORD dataset:
  https://github.com/clovaai/cord

- SROIE:
  https://github.com/zzzDavid/ICDAR-2019-SROIE

- FUNSD:
  https://guillaumejaume.github.io/FUNSD/
