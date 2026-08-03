from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Date, ForeignKey
from datetime import date

class Base(DeclarativeBase):
    pass

class Vendor(Base):
    __tablename__ = "vendor"
    vendor_id: Mapped[int] = mapped_column(primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(100))
    tax_id: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(200))
    contact_information: Mapped[str] = mapped_column(String(100))
    invoices: Mapped[list["Invoice"]] = relationship(back_populates="vendor")

class Invoice(Base):
    __tablename__ = "invoice"
    invoice_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(50))
    vendor_id: Mapped[int] = mapped_column(ForeignKey("vendor.vendor_id"))
    invoice_date: Mapped[date] = mapped_column(Date)
    due_date: Mapped[date] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String(10))
    purchase_order_number: Mapped[str] = mapped_column(String(50))
    payment_terms: Mapped[str] = mapped_column(String(50))
    line_items = relationship("LineItem", backref="invoice")
    tax_total: Mapped[float] = mapped_column(Float)
    subtotal: Mapped[float] = mapped_column(Float)
    discount_total: Mapped[float] = mapped_column(Float)
    shipping_total: Mapped[float] = mapped_column(Float)
    grand_total: Mapped[float] = mapped_column(Float)
    vendor: Mapped["Vendor"] = relationship(back_populates="invoices")

class LineItem(Base):
    __tablename__ = "line_item"
    line_item_id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoice.invoice_id"))
    description: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[float] = mapped_column(Float)
    unit_price: Mapped[float] = mapped_column(Float)
    total_price: Mapped[float] = mapped_column(Float)