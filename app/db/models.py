from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class InvoiceSequence(Base):
    __tablename__ = 'invoice_sequence'

    id = Column(Integer, primary_key=True)
    invoice_prefix = Column(VARCHAR(256), nullable=False)
    last_sequence_number = Column(Integer, nullable=False)
