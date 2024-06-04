# Stori Transactions Email Generator

# Overview

This application allow users to send account balance emails, containing:
- The account total balance.
- Average debit amount.
- Average credit amount.
- Number of transactions per month.

The input file format accepted is as follows:


Required fields in the CSV file:
- `Id`: unique id for the account.
- `Date`: date in format `month/day`.
- `Transactions`: user transaction amounts, where `+` sign denotes a credit transactions and `-` sign denotes a debit transaction.

Expected email format:
![Expected email format](/assets/email_example.png "Expected email format")


# Local Environment Setup

## Requirements
- Python 3.9
- [Docker Desktop (Optional)](https://www.docker.com/products/docker-desktop/)
- [Docker Compose (Optional)](https://pypi.org/project/docker-compose/)


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

With the image `transactions-email-generator-app` built and running, execute the following command to process a file in a mounted directory (`csv` folder in this repository):
```bash
docker run \
    -v ./csv:/csv \
    transactions-email-generator-app:latest \
    --client_name "Abraham Montoya" \
    --subject "Your Stori's Account Balance!" \
    --recipient "montoyaobeso@gmail.com" \
    --path-to-file "/csv/transactions_1.csv"
```

# API Description

## Overview
This API is designed to process CSV files containing debit and credit transactions, providing a seamless way to calculate balances and send HTML-formatted email summaries to end users. The input file format should contain three columns: `Id`, `Date`, and `Transaction`. The `Date` is formatted as `MM/DD`, and transactions are identified by a `+` sign (credit) and a `-` sign (debit).

## Input File Format

The CSV file should have the following columns:

- `Id`: A unique identifier for each transaction.
- `Date`: The date of the transaction in `MM/DD` format.
- `Transaction`: The transaction amount, prefixed with `+` for creadit and `-` for debit.


CSV file example
```csv
Id,Date,Transaction
0,7/11,+60.5
1,7/28,-10.3
2,8/23,-20.46
3,8/13,+10
```

## Endpoints

### Process Large Files (>10MB)

1. Get a presigend URL

   **Endpoint:** `/presigned_url`
   
   **Method:** `GET`
   
   **Description:** Use this endpoint to get a presigned URL to upload large CSV files to S3. After uploading, the file will be processed through the `/balance_by_file_id` endpoint. 

   **Response:** A dict with the presigned url and access keys to upload the file.
   

   **Steps:**
   1. Send a POST request to `/presigned_url` to obtain a pre-signed URL for file upload.
   2. Upload the CSV file to the provided S3 URL.
   3. Use the `/balance_by_file_id` endpoint to process the file and send the email.

2. Process Uploaded File (>10MB)

   **Endpoint:** `/balance_by_file_id`
   
   **Method:** `POST`
   
   **Description:** Process a previously uploaded CSV file by its file ID.
   
   **Request Fields:**
   - `client_name` (string): The name of the client.
   - `recipient` (string): The recipient's email address.
   - `subject` (string): The subject line for the email.
   - `file_id` (string): The ID of the file uploaded to S3.

   **Response:** An HTML-formatted email is sent to the recipient containing the balance summary.

### Process Small Files (<10MB)

   **Endpoint:** `/balance_by_file`
   
   **Method:** `POST`
   
   **Description:** Use this endpoint to upload and process small CSV files (less than 10MB) directly.
   
   **Request Fields:**
   - `file` (binary): The CSV file to be processed.
   - `client_name` (string): The name of the client.
   - `recipient` (string): The recipient's email address.
   - `subject` (string): The subject line for the email.

   **Response:** An HTML-formatted email is sent to the recipient containing the balance summary.






## Endpoints summary

The available endpoints are as follows:

| Endpoint            | Method | Description                                                                                                             | Input    | Output                                                                           |
|---------------------|--------|-------------------------------------------------------------------------------------------------------------------------|----------|----------------------------------------------------------------------------------|
| `/`                   | GET    | Root endpoint.                                                                                                          | NA       | A welcome message, the API is running and accepting requests.                 |
| `/presigned_url`      | GET    | Get an URL to post a file bigger than 10Mb. Note: it is required to use an external tool to post the file to s3 (i.e. Postman, or the `requests` module).                                                                            | NA       | A dict with `url` and `fields` to upload a file to s3.                           |
| `/balance_by_file_id` | POST    | Post a file processing request of a previously uploaded file using the presigned URL obtained through `/presigned_url`. | `client_name`, `recipient`, `subject`, `file_id` | A message informing the email was send sucessfully, or an error message instead. |
| `/balance_by_file` | POST    | Post a file processing request by providing the file (size limit is <10Mb) | `client_name`, `recipient`, `subject`, `file` | A message informing the email was send sucessfully, or an error message instead. |


## Post a file to `/balance_by_file_id` using a `presigned_url`:

```python
import requests

"""
Script to get a presigned URL, upload a file to s3 and send a balance summary with the uploaded file.
"""

HOST = "https://rkes7qxbb0.execute-api.us-west-2.amazonaws.com"  # Dev environment
# HOST = "http://127.0.0.1/"  # Local environment
PATH_TO_FILE = "csv/transactions_1M.csv"  # 1 million records file ~18Mb


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
print("File uploaded...")

# Call send balance endpoint with key id
print("Requesting the file processing by its id.")
http_response = requests.post(
    f"{HOST}/balance_by_file_id",
    data={
        "client_name": "Abraham Montoya",
        "recipient": "montoyaobeso@gmail.com",
        "subject": "Your Stori's Account Balance (balance_by_file_id)!",
        "file_id": presigned_url_info["fields"]["key"],
    },
)

print("Response: ", http_response.content)
```

## Post a file to `/balance_by_file`:
```python
import requests

"""
Script to send a balance summary by posting a file.
"""

HOST = "https://rkes7qxbb0.execute-api.us-west-2.amazonaws.com"  # Dev environment
# HOST = "http://127.0.0.1"  # Local environment
PATH_TO_FILE = "csv/transactions_1.csv"  # File with a few records

# Read file
with open(PATH_TO_FILE, "rb") as f:
    filebody = f.read()

# Call send balance with binary file
http_response = requests.post(
    f"{HOST}/balance_by_file",
    data={
        "client_name": "Abraham Montoya",
        "recipient": "montoyaobeso@gmail.com",
        "subject": "Your Stori's Account Balance (balance_by_file)!",
    },
    files={
        "file": (
            PATH_TO_FILE.split("/")[-1],
            filebody,
            "text/csv",
        ),
    },
)

print("Response:", http_response.content)
```