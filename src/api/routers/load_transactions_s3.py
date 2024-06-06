import io
import os
from typing import Annotated

import boto3
import pandas as pd
import pandera as pa
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.app.db import crud, schemas
from src.app.db.database import SessionLocal
from src.app.validator.input_validator import schema

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


@router.post("/load_transactions_s3")
async def load_transactions_s3(
    account_id: Annotated[
        str,
        Form(
            description="The account id.",
        ),
    ],
    file_id: Annotated[
        str,
        Form(
            description="File ID genereated by /presigned_url endpoint.",
        ),
    ],
    db: Session = Depends(get_db),
):
    """Load transactions from a file uploaded to s3."""

    # Create s3 client and get object
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=os.environ["BUCKET_NAME"], Key=file_id)

    txns = pd.read_csv(io.BytesIO(obj["Body"].read()), encoding="latin1")

    try:
        txns = schema.validate(txns, lazy=True)

    except pa.errors.SchemaErrors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "The input file is not formated correctly, please review it."
            },
        )

    transactions = [
        schemas.TransactionCreate(
            transaction_id=t["Id"],
            date=t["Date"],
            value=t["Transaction"],
        )
        for t in (txns.to_dict("records"))
    ]

    db_account = crud.get_account(db, account_id=account_id)

    if db_account is None:
        raise HTTPException(status_code=400, detail="Account not found.")

    # Save transactions

    crud.save_transactions_bulk(
        db,
        transactions=transactions,
        account_id=db_account.id,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "File processed successfuly.",
            # "saved": saved_records,
            # "ignored": ignored_records,
            # "total": saved_records + ignored_records,
        },
    )

    # # Get transactions processor
    # tp = TransactionsProcessor(transactions=txns)

    # body_builder = EmailBodyBuilder(
    #     client_name=client_name,
    #     total_balance=tp.get_balance(),
    #     avg_credit_amount=tp.get_avg_credit_amount(),
    #     avg_debit_amount=tp.get_avg_debit_amount(),
    #     transactions_per_month=tp.get_montly_transactions(),
    # )

    # email_sender = EmailSender(
    #     subject=subject,
    #     recipient=recipient,
    #     body_content=body_builder.get_email_body(),
    # )

    # email_sender.send_email()
