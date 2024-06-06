from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    Double,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, index=True)
    date = Column(Date, index=True)
    value = Column(Double, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="items")

    __table_args__ = (
        UniqueConstraint("transaction_id", "account_id", name="_unique_transaction_id"),
    )
