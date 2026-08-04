from sqlalchemy import create_engine
from invoiceIQ.infrastructure.database.models import Base,Vendor, Invoice, LineItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


engine = create_engine("sqlite:///invoiceiq.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


session = SessionLocal()
vendor = Vendor(
    legal_name="ABC Technologies",
    tax_id="GST123",
    address="Bengaluru",
    contact_information="John Doe, john.doe@abc.com"
)

try:
    session.add(vendor)
    session.commit()
except:
    session.rollback()
    raise
finally:
    print(vendor.vendor_id)
    session.close()

statement = select(Vendor)

result = session.execute(statement)

vendors = result.scalars().all()

for vendor in vendors:
    print(vendor.vendor_id)
    print(vendor.legal_name)
statement = select(Vendor).where(Vendor.vendor_id == 1)

vendor = session.execute(statement).scalar_one_or_none()

print(vendor)
