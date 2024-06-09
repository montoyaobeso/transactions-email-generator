from datetime import date
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.app.db import crud
from src.app.db.dependencies import get_db
from src.app.email.content_builder import EmailBodyBuilder
from src.app.email.sender import EmailSender
from src.app.transactions.processor import TransactionsProcessor

router = APIRouter(
    prefix="/send_balance",
    tags=["send_balance"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def send_balance(
    account_id: Annotated[
        str,
        Form(
            description="The client's name.",
        ),
    ],
    from_date: Annotated[
        date,
        Form(
            description="Date to recover records from (lower limit, inclusive). Format `YYYY-MM-DD`."
        ),
    ] = None,
    to_date: Annotated[
        date,
        Form(
            description="Date to recover records to (upper lmit, inclusive. Format `YYYY-MM-DD`."
        ),
    ] = None,
    db: Session = Depends(get_db),
):
    """Send balance to account's email."""

    # Get account info
    db_account = crud.get_account(db, account_id=account_id)

    if db_account is None:
        raise HTTPException(status_code=400, detail="Account not found.")

    # Get all transactions for the given account_id
    db_transactions = crud.get_transactions_by_date(
        db,
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
    )

    if db_transactions is None:
        raise HTTPException(status_code=400, detail="Account not found.")

    # Create a DataFrame from the list of dictionaries
    transactions_df = pd.DataFrame([model.model_dump() for model in db_transactions])

    # Get transactions processor
    tp = TransactionsProcessor(transactions=transactions_df)

    body_builder = EmailBodyBuilder(
        client_name=db_account.name,
        total_balance=tp.get_balance(),
        avg_credit_amount=tp.get_avg_credit_amount(),
        avg_debit_amount=tp.get_avg_debit_amount(),
        transactions_history=tp.get_transactions_history(),
    )

    email_sender = EmailSender(
        subject="Your Account Balance!",
        recipient=db_account.email,
        body_content=body_builder.get_email_body(),
    )

    email_sender.send_email()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Email sent succesfully."},
    )
