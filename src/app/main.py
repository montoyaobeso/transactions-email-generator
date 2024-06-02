import argparse
from src.app.email.content_builder import get_email_body
from src.app.email.sender import SendEmailService

import src.app.exceptions as app_exceptions
import pandas as pd
import pandera as pa
from src.app.transactions.processor import TransactionsProcessor
from src.app.validator.input_validator import schema

from dotenv import load_dotenv

load_dotenv()


def create_parser():
    parser = argparse.ArgumentParser(
        description="Stori Account Balance Email Sender CLI."
    )
    parser.add_argument(
        "-n",
        "--client_name",
        help="Display client name.",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--recipient",
        help="Email recipient.",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--subject",
        help="Email subject.",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--path-to-file",
        help="Path to CSV file.",
        required=True,
    )
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Validat input file format
    if not args.path_to_file.lower().endswith(".csv"):
        raise app_exceptions.IncorrectInputFileFormat(args.path_to_file)

    # Read file and validate content
    try:
        df = schema.validate(pd.read_csv(args.path_to_file), lazy=True)
    except pa.errors.SchemaErrors as error:
        raise app_exceptions.SchemaValidationErrorException(error)

    # Get transactons processor
    tp = TransactionsProcessor(df)

    # Get email body
    email_body = get_email_body(
        client_name=args.client_name,
        total_balance=tp.get_balance(),
        avg_credit_amount=tp.get_avg_credit_amount(),
        avg_debit_amount=tp.get_avg_debit_amount(),
        transactions_per_month=tp.get_montly_transactions(),
    )

    SendEmailService().send_email(
        subject=args.subject,
        recipient=args.recipient,
        body_content=email_body,
    )

    print("Email send succesfully.")


if __name__ == "__main__":
    main()
