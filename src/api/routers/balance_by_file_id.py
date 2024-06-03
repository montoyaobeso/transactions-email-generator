import io
import os
from typing import Annotated

import pandas as pd
import pandera as pa
from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import JSONResponse

import boto3
import io


from src.app.email.content_builder import get_email_body
from src.app.email.sender import SendEmailService
from src.app.transactions.processor import TransactionsProcessor
from src.app.validator.input_validator import schema

router = APIRouter(
    prefix="/balance_by_file_id",
    tags=["balance_by_file_id"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def balance_by_file_id(
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
    file_id: Annotated[
        str,
        Form(
            description="File ID genereated by /presigned_url endpoint.",
        ),
    ],
):

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

    # Get transactions processor
    tp = TransactionsProcessor(transactions=txns)

    email_body = get_email_body(
        client_name=client_name,
        total_balance=tp.get_balance(),
        avg_credit_amount=tp.get_avg_credit_amount(),
        avg_debit_amount=tp.get_avg_debit_amount(),
        transactions_per_month=tp.get_montly_transactions(),
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
