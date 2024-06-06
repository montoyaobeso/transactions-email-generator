# Stori Transactions Email Generator

# Overview

This application offers a solution for managing and reporting on account balances.

## Key Features
### Email Notifications

Users can send comprehensive account balance emails, including:

- **Total Account Balance**: The overall balance of the account.
- **Average Debit Amount**: The average amount of all debit transactions.
- **Average Credit Amount**: The average amount of all credit transactions.
- **Monthly Transaction Count**: The number of transactions processed each month.


### CSV Input File

The application requires detailed CSV files containing the following columns:

- `Id`: A unique identifier for each transaction.
- `Date`: The transaction date in MM/DD/YYYY format.
- `Transaction`: The amount of the transaction, marked with + for credits and - for debits.

### Command Line Interface (CLI)

A simple CLI is available, offering:
 - **Account managment**: create accounts.
 - **Load account transactions**: load transactions to database though CSV provided files.
 - **Send balance**: notify users by sending custom emails with detailed data.

### API Deployment

The API is deployed on AWS, providing:

AWS Integration: Works seamlessly with other AWS services, such as:
- **AWS S3**: For storing and retrieving CSV files.
- **AWS SecretsManager**: For secure credentials storage.
- **AWS RDS (PostgreSQL)**: For robust database management.

# Local Environment Setup

## Requirements
- [Python 3.9](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://pypi.org/project/docker-compose/)


## Setup
Create a virtual environment:


```bash
python3.9 -m venv venv
```

Activate the environemnt:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the email sender service credentials:
```bash
cp .env.example .env
```

Set `SENDGRID_SENDER_EMAIL` and `SENDGRID_API_KEY` to enable sending emails trough SendGrid service.



Once all dependencies are installed there are two options to run the server, could be executed locally or in a docker container.

Build images with docker compose:
```bash
 docker compose up --build --force-recreate --detach
 ```
 Be sure the docker daemon is running.


# Command Line Interface

The CLI allows three diffent flows:
- `create_account`: register a new account to the database.
- `load_transactions`: register account related transactions.
- `send_balance`: send a balance summary to account's registered email.


CLI Help:
```bash
$ docker run -v ./csv:/csv transactions-email-generator-app:latest -h
usage: cli.py [-h] {create_account,load_transactions,send_balance} ...

A command line tool with multiple flows.

positional arguments:
  {create_account,load_transactions,send_balance}
                        Choose the flow to execute
    create_account      Execute create_account flow. Requires parameters
                        --name (str) and --email (str)
    load_transactions   Execute load_transactions flow. Requires parameters
                        --account_id and --path-to_file
    send_balance        Execute send_email flow. Requires parameters
                        --account_id, --from_date and --to_date

optional arguments:
  -h, --help            show this help message and exit
```

# API Description

With the image `transactions-email-generator-app` built and running the following flows can be executed:
### Create Account
```bash
docker run -v ./csv:/csv transactions-email-generator-app:latest create_account --name "Stori Card" --email storinoreply@gmail.com
```

### Load Transactions
```bash
docker run -v ./csv:/csv transactions-email-generator-app:latest load_transactions --account-id 1 --path-to-file /csv/transactions_10k.csv
```

### Send Balance
```bash
docker run -v ./csv:/csv transactions-email-generator-app:latest send_balance --account-id 1
```

## Endpoints

# API Description

## Endpoints

The available endpoints are as follows:

| Endpoint            | Method | Description                                                                                                             | Parameters    | Output                                                                           |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------|
| `/`                   | GET    | Root endpoint.                                                                                                          | NA       | A welcome message, the API is running and accepting requests.                 |
| `/presigned_url`      | GET    | Get an URL to post a file bigger than 10Mb. Note: it is required to use an external tool to post the file to s3 (i.e. Postman, or the `requests` module).                                                                            | NA       | A dict with `url` and `fields` to upload a file to s3.                           |
| `/load_transactions_s3` | POST    | Post a request to save transactions from a previously uploaded file using the presigned URL obtained through `/presigned_url`. | `account_id` and `file_id` | A message informing the file was successfully processed or an error message instead.  |
| `/load_transactions` | POST    | Post a file processing request by providing the file (size limit is <10Mb) | `account_id` and `file` | A message informing the file was successfully processed or an error message instead. |
| `/send_balance` | POST    | Post a request to gather account transactions and send a balance summary to account's email. | `account_id` | A message informing the email was send sucessfully, or an error message instead. |


Script to post a file to presigned url:

```python
import requests

"""
Script to get a presigned URL and upload a file to s3.
"""

HOST = "https://rkes7qxbb0.execute-api.us-west-2.amazonaws.com"  # Dev environment
# HOST = "http://127.0.0.1/"  # Local environment
PATH_TO_FILE = "csv/transactions_1.csv"

# Get presigned URL
presigned_url_info = requests.get(f"{HOST}/presigned_url").json()

# Upload the file to the presigned URL
with open(PATH_TO_FILE, "rb") as f:
    filebody = f.read()

print("Uploading file to s3...")
upload_response = requests.post(
    presigned_url_info["url"],
    data=presigned_url_info["fields"],
    files={
        "file": (
            presigned_url_info["fields"]["key"],
            filebody,
            "text/csv",
        )
    },
)
print("File uploaded with file_id: ", presigned_url_info["fields"]["key"])

```
