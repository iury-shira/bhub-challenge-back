from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    corporate_name = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    declared_billing = Column(Integer)

    bank_data = relationship("BankData", back_populates="owner", cascade="all, delete")


class BankData(Base):
    __tablename__ = "bank_data"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    agency = Column(String, nullable=False)
    account = Column(String, nullable=False, unique=True)
    bank = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))

    owner = relationship("Client", back_populates="bank_data")

