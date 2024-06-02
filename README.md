# Stori Transactions Email Generator

This application allow users to send account balance emails, containing:
- The total balance
- Average debit amount
- Average credit amount
- Number of transactions per month

The input file format accepted is as follows:
```csv
Id,Date,Transaction
0,7/11,+60.5
1,7/28,-10.3
2,8/23,-20.46
3,8/13,+10
```

Fields in the CSV file:
- `Id`: unique id for the account.
- `Date`: date in format `month/day`.
- `Transactions`: user transaction amounts, where `+` sign denotes a credit transactions and `-` sign denotes a debit transaction.

Expected email format:
![Expected email format](/assets/email_example.png "Expected email format")


# Local execution

## Requirements
- Python 3.9
- [Docker Desktop (Optional)](https://www.docker.com/products/docker-desktop/)
- [Docker Compose (Optional)](https://pypi.org/project/docker-compose/)


## Environment setup
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

Run the server in a Docker container:
```bash
 docker compose up --build --force-recreate --detach
 ```
 Be sure the docker daemon is running.

With the image `transactions-email-generator-app` built, execute the following to process a file in a mounted directory:
```bash
docker run \
    -v ./csv:/csv \
    transactions-email-generator-app:latest \
    --client_name "Abraham Montoya" \
    --subject "Stori's Account Balance" \
    --recipient "montoyaobeso@gmail.com" \
    --path-to-file "/csv/transactions_1.csv"
```


 In order to run the `uvicorn` server locally, see for changes and continue developing new features, run:
```bash
uvicorn src.api.main:app --reload --port 80
```


 If everything is working properly you should see something like this:
 ```bash
INFO:     Will watch for changes in these directories: ['~/transactions-email-generator']
INFO:     Uvicorn running on http://127.0.0.1:80 (Press CTRL+C to quit)
INFO:     Started reloader process [23452] using WatchFiles
INFO:     Started server process [23454]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```


# API

Add a table of the available endpoints.

# Local testing

With the server running (locally or ina docker container), you can access the documentation and test the application from http://127.0.0.1/docs.

Add the postman collection.


A `curl` example to post to the `send_summary` endpoint and give all form input data and the CSV input file:
```bash
curl -X 'POST' \
  'http://127.0.0.1/send_summary' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'client_name=Abraham Montoya' \
  -F 'recipient=montoyaobeso@gmail.com' \
  -F 'subject=Stori'\''s Account Balance!' \
  -F 'file=@csv/transactions_1.csv;type=text/csv'
```

Response:
```bash
{"message":"Email sent succesfully."}
```