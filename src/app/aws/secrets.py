import boto3
from botocore.exceptions import ClientError
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(secret_name: str, region: str = "us-west-2"):

    logging.info(f"Trying to get secret {secret_name}")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = get_secret_value_response["SecretString"]

    logging.info("Secret retrieved successfully.")

    return json.loads(secret)
