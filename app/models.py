from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class Client(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    corporate_name = Column(String)
    phone_number = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    declared_billing = Column(Integer)
