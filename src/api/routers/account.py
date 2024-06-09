from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.db import crud, schemas
from src.app.db.database import SessionLocal

router = APIRouter(
    prefix="",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from typing import Annotated


@router.post("/account", response_model=schemas.Account)
async def create_account(
    account: schemas.AccountCreate,
    db: Session = Depends(get_db),
):
    """Create a new account."""
    # Get account by email
    db_account = crud.get_account_by_email(db, email=account.email)

    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_account(db, account=account)


@router.get("/accounts", response_model=List[schemas.Accounts])
async def get_accounts(db: Session = Depends(get_db)):
    """Get all accounts."""

    # Get account by email
    db_account = crud.get_accounts(db)

    if db_account is None:
        raise HTTPException(status_code=400, detail="No accounts found.")

    return db_account
