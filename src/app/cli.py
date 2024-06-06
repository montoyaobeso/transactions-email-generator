import argparse
from functools import wraps

import pandas as pd
import pandera as pa
from dotenv import load_dotenv

load_dotenv()

import src.app.exceptions as app_exceptions
from src.app.db import crud, schemas
from src.app.db.database import SessionLocal
from src.app.email.content_builder import EmailBodyBuilder
from src.app.email.sender import EmailSender
from src.app.transactions.processor import TransactionsProcessor
from src.app.validator.input_validator import schema


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionLocal()
        try:
            result = func(*args, session=session, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return wrapper


@with_session
def create_account_flow(args, session):
    """Create a new account."""

    account = schemas.AccountCreate(name=args.name, email=args.email)

    # Get account by email
    db_account = crud.get_account_by_email(session, email=account.email)

    if db_account:
        raise app_exceptions.AccountAlreadyExistsInDBException()

    db_account = crud.create_account(session, account=account)

    print(db_account.model_dump())


@with_session
def load_transactions_flow(args, session):
    """Load transactions to database."""

    db_account = crud.get_account(session, account_id=args.account_id)

    txns = pd.read_csv(args.path_to_file, encoding="latin1")

    # Validat input file format
    if not args.path_to_file.lower().endswith(".csv"):
        raise app_exceptions.IncorrectInputFileFormat(args.path_to_file)

    try:
        txns = schema.validate(pd.read_csv(args.path_to_file), lazy=True)
    except pa.errors.SchemaErrors as error:
        raise app_exceptions.SchemaValidationErrorException(error)

    if db_account is None:
        raise app_exceptions.AccountAlreadyExistsInDBException()

    transactions = [
        schemas.TransactionCreate(
            transaction_id=t["Id"],
            date=t["Date"],
            value=t["Transaction"],
        )
        for t in (txns.to_dict("records"))
    ]

    crud.save_transactions_bulk(
        session,
        transactions=transactions,
        account_id=db_account.id,
    )

    print("File processed successfully")


@with_session
def send_balance_flow(args, session):
    """Send balance to account's registered email."""
    # Get account info
    db_account = crud.get_account(session, account_id=args.account_id)

    if db_account is None:
        raise app_exceptions.AccountAlreadyExistsInDBException()

    # Get all transactions for the given account_id
    db_transactions = crud.get_transactions_by_date(
        session,
        account_id=args.account_id,
        from_date=args.from_date,
        to_date=args.to_date,
    )

    if db_transactions is None:
        raise app_exceptions.TransactionsNotFound()

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

    print(f"Email send successfully to {db_account.email}!")


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="A command line tool with multiple flows."
    )

    # Create subparsers for different flows
    subparsers = parser.add_subparsers(
        dest="flow",
        help="Choose the flow to execute",
    )

    # Create account flow
    parser_flow_one = subparsers.add_parser(
        "create_account",
        help="Execute create_account flow. Requires parameters --name (str) and --email (str)",
    )
    parser_flow_one.add_argument(
        "--name",
        type=str,
        help="User account name.",
        required=True,
    )
    parser_flow_one.add_argument(
        "--email",
        type=str,
        help="Account email.",
        required=True,
    )
    parser_flow_one.set_defaults(func=create_account_flow)

    # Load transactions flow
    parser_load_transactions = subparsers.add_parser(
        "load_transactions",
        help="Execute load_transactions flow. Requires parameters --account_id and --path-to_file",
    )
    parser_load_transactions.add_argument(
        "--account-id",
        type=str,
        help="Account id.",
        required=True,
    )
    parser_load_transactions.add_argument(
        "--path-to-file",
        type=str,
        help="Path to CSV file.",
        required=True,
    )
    parser_load_transactions.set_defaults(func=load_transactions_flow)

    # Send balance flow
    parser_send_balance = subparsers.add_parser(
        "send_balance",
        help="Execute send_email flow. Requires parameters --account_id, --from_date and --to_date",
    )
    parser_send_balance.add_argument(
        "--account-id",
        type=str,
        help="Account id.",
        required=True,
    )
    parser_send_balance.add_argument(
        "--from_date",
        type=str,
        help="From date to consider records in format YYYY-MM-DD",
        required=False,
        const=None,
    )
    parser_send_balance.add_argument(
        "--to_date",
        type=int,
        help="To date to consider records in format YYYY-MM-DD",
        const=None,
    )
    parser_send_balance.set_defaults(func=send_balance_flow)

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the flow
    if args.flow:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
