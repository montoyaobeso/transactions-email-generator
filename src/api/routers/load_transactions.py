import io
from typing import Annotated

import pandas as pd
import pandera as pa
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, Depends
from fastapi.responses import JSONResponse

from src.app.db import crud, schemas
from src.app.db.database import SessionLocal
from src.app.validator.input_validator import schema
from sqlalchemy.orm import Session

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


@router.post("/load_transactions")
async def load_transactions(
    account_id: Annotated[
        str,
        Form(
            description="The account id.",
        ),
    ],
    file: UploadFile = File(..., description="Binary CSV file data."),
    db: Session = Depends(get_db),
):

    db_account = crud.get_account(db, account_id=account_id)

    if file.content_type == "text/csv":
        txns = pd.read_csv(io.BytesIO(await file.read()), encoding="latin1")

        try:
            txns = schema.validate(txns, lazy=True)
        except pa.errors.SchemaErrors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "The input file is not formated correctly, please review it."
                },
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": f"Only CSV files are supported, you provided {file.filename}."
            },
        )

    if db_account is None:
        raise HTTPException(status_code=400, detail="Account not found.")

    transactions = [
        schemas.TransactionCreate(
            transaction_id=t["Id"],
            date=t["Date"],
            value=t["Transaction"],
        )
        for t in (txns.to_dict("records"))
    ]

    # Save transactions
    ignored_records = 0
    saved_records = 0
    for txn in transactions:
        db_transaction = crud.get_transaction_by_ids(
            db,
            account_id=account_id,
            transaction_id=txn.transaction_id,
        )
        if db_transaction:
            ignored_records += 1
            continue

        crud.create_transaction(db, transaction=txn, account_id=db_account.id)
        saved_records += 1

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "File processed successfuly.",
            "saved": saved_records,
            "ignored": ignored_records,
            "total": saved_records + ignored_records,
        },
    )
