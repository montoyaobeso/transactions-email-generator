from sqlalchemy.orm import Session

from . import models, schemas

from datetime import date

from typing import List


from pydantic import parse_obj_as
from src.app.db.database import engine


def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate):
    db_item = models.Account(email=account.email, name=account.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def get_transactions_by_date(
    db: Session,
    account_id: int,
    from_date: date = None,
    to_date: date = None,
) -> List[schemas.Transaction]:
    if from_date is None and to_date is None:
        return parse_obj_as(
            List[schemas.Transaction],
            (
                db.query(models.Transaction)
                .filter(models.Transaction.account_id == account_id)
                .all()
            ),
        )

    if from_date is not None and to_date is None:
        return parse_obj_as(
            List[schemas.Transaction],
            (
                db.query(models.Transaction)
                .filter(models.Transaction.account_id == account_id)
                .filter(models.Transaction.date >= from_date)
                .all()
            ),
        )

    if from_date is None and to_date is not None:
        return parse_obj_as(
            List[schemas.Transaction],
            (
                db.query(models.Transaction)
                .filter(models.Transaction.account_id == account_id)
                .filter(models.Transaction.date <= to_date)
                .all()
            ),
        )

    if from_date is not None and to_date is not None:
        return parse_obj_as(
            List[schemas.Transaction],
            (
                db.query(models.Transaction)
                .filter(models.Transaction.account_id == account_id)
                .filter(models.Transaction.date >= from_date)
                .filter(models.Transaction.date <= to_date)
                .all()
            ),
        )


def get_transaction_by_ids(
    db: Session, account_id: int, transaction_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.transaction_id == transaction_id)
        .filter(models.Transaction.account_id == account_id)
        .first()
    )


def get_transactions_by_account_id(
    db: Session, account_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.account_id == account_id)
        .all()
    )


def create_transaction(
    db: Session, transaction: schemas.TransactionCreate, account_id: int
):
    db_item = models.Transaction(**transaction.model_dump(), account_id=account_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


from src.app.db.models import Transaction as TransactionTable
from sqlalchemy.dialects.postgresql import insert


def save_transactions_bulk(
    db: Session, transactions: List[schemas.TransactionCreate], account_id: int
):
    data = [
        {
            "transaction_id": t.transaction_id,
            "date": t.date,
            "value": t.value,
            "account_id": account_id,
        }
        for t in transactions
    ]

    insert_table = insert(TransactionTable).values(data)
    insert_table_sql = insert_table.on_conflict_do_nothing(
        index_elements=["transaction_id", "account_id"]
    )

    db.execute(insert_table_sql)
    db.commit()
