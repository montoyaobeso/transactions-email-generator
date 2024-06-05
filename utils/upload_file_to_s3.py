import requests

"""
Script to get a presigned URL, upload a file to s3 and send a balance summary with the uploaded file.
"""

HOST = "https://rkes7qxbb0.execute-api.us-west-2.amazonaws.com"  # Dev environment
# HOST = "http://127.0.0.1/"  # Local environment
PATH_TO_FILE = "csv/transactions_1M.csv"  # 1 million records file ~18Mb


# Get presigned URL
presigned_url_info = requests.get(f"{HOST}/presigned_url").json()

print(presigned_url_info)

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

print("File id: ", presigned_url_info["fields"]["key"])
