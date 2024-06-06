from typing import Union, Literal
from datetime import date
from pydantic import BaseModel, EmailStr, Field


# Transaction schemas
class TransactionBase(BaseModel):
    transaction_id: int
    date: date
    value: float


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    account_id: int

    class Config:
        from_attributes = True


class Transactions(TransactionBase):
    id: int


# Account schemas
class AccountBase(BaseModel):
    name: str
    email: EmailStr


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    is_active: bool
    items: list[Transaction] = []

    class Config:
        from_attributes = True


class Accounts(AccountBase):
    id: int
    is_active: bool
