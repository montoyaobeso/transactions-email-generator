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

<img src="/assets/email_example.png" alt="MarineGEO circle logo" style="height: 100px;"/>


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

Once all dependencies are installed there are two options to run the server, locally or in a docker container.

Run the server locally:
```bash
 uvicorn src.app.main:app --reload --port 80
```

Run the server in a Docker container:
```bash
 docker compose up --build --force-recreate
 ```
 Be sure the docker daemon is running.


 # Local testing
