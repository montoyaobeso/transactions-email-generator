import json

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name: str, region: str = "us-west-2"):
    """Get a secret value from AWS SecretsManager service."""

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = get_secret_value_response["SecretString"]

    return json.loads(secret)
