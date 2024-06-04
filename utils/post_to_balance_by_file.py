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
