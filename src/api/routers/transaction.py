from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.db import crud, schemas
from src.app.db.database import SessionLocal

router = APIRouter(
    prefix="",
    tags=["transaction"],
    responses={404: {"description": "Not found"}},
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transaction", response_model=schemas.Transaction)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    account_id: int,
    db: Session = Depends(get_db),
):
    """Register a single transaction."""
    db_transaction = crud.get_transaction_by_ids(
        db, account_id=account_id, transaction_id=transaction.transaction_id
    )

    if db_transaction:
        raise HTTPException(
            status_code=400, detail="Transaction is already registered."
        )

    return crud.create_transaction(db, transaction=transaction, account_id=account_id)


@router.get("/transactions", response_model=List[schemas.Transactions])
async def get_transactions(
    account_id: int,
    db: Session = Depends(get_db),
):
    """Get all transactions."""
    db_transaction = crud.get_transactions_by_account_id(db, account_id=account_id)

    if db_transaction is None:
        raise HTTPException(status_code=400, detail="Transactions not found.")

    return db_transaction
