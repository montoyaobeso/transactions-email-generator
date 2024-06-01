import io
import os
from typing import Annotated

import pandas as pd
import pandera as pa
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from src.app.email.content_builder import get_email_body
from src.app.email.sender import SendEmailService
from src.app.transactions.processor import TransactionsProcessor
from src.app.validator.input_validator import schema

router = APIRouter(
    prefix="/send_summary",
    tags=["send_summary"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def send_summary(
    client_name: Annotated[
        str,
        Form(
            description="The client's name.",
        ),
    ],
    recipient: Annotated[
        str,
        Form(
            description="The recipient email.",
        ),
    ],
    subject: Annotated[
        str,
        Form(
            description="Email subject.",
        ),
    ],
    file: UploadFile = File(..., description="Binary CSV file data."),
):
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

        # Get transactions processor
        ts = TransactionsProcessor(transactions=txns)

    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": f"Only CSV files are supported, you provided {file.filename}."
            },
        )

    email_body = get_email_body(
        client_name=client_name,
        total_balance=ts.get_balance(),
        avg_credit_amount=ts.get_avg_credit_amount(),
        avg_debit_amount=ts.get_avg_debit_amount(),
        transactions_per_month=ts.get_montly_transactions(),
    )

    SendEmailService().send_email(
        subject=subject,
        recipient=recipient,
        body_content=email_body,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Email sent succesfully."},
    )
