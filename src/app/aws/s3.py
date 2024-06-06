import logging

import boto3
from botocore.exceptions import ClientError


def create_presigned_post(
    bucket_name, object_name, fields=None, conditions=None, expiration=3600
):
    """Generate a presigned URL S3 POST request to upload a file"""

    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response
