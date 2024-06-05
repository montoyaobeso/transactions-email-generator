import os
from unittest import TestCase
from unittest.mock import patch

import boto3
from botocore.response import StreamingBody
from botocore.stub import Stubber
from fastapi import status
from fastapi.testclient import TestClient

from src.api.main import app
from src.app.email.sender import EmailSender

# Replace bucket name in env variables
os.environ["BUCKET_NAME"] = "my-bucket"


def mock_send_email(cls, *args, **kwargs):
    print("send_email funcion mocked")
    return None


# class TestBalanceByFileId(TestCase):
#     client = TestClient(app)
#     AwsRegion = "us-west-2"
#     AwsAccessKey = "access-key"
#     AwsSecretKey = "secret-key"
#     AwsServiceName = "S3"

#     # AWS S3 Resources
#     AwsS3BucketName: str = "my-bucket"
#     AwsS3UrlKey: str = "transactions_1.csv"

#     def setUp(self) -> None:
#         """Request resources before the unit test execution."""
#         self.__botoClientS3 = boto3.client(
#             self.AwsServiceName.lower(),
#             aws_access_key_id=self.AwsAccessKey,
#             aws_secret_access_key=self.AwsSecretKey,
#             region_name=self.AwsRegion,
#             endpoint_url=f"https://{self.AwsServiceName.lower()}.{self.AwsRegion}.amazonaws.com",
#         )

#         self.__botoClientStubberS3 = Stubber(self.__botoClientS3)
#         self.__botoClientStubberS3.activate()

#     def tearDown(self) -> None:
#         """Release requested resoruces after the unit test execution."""
#         self.__botoClientStubberS3.deactivate()

#     def mocksS3GetObject(self, data) -> None:
#         """
#         Mocks the AWS S3 service `get_object`.
#         """
#         s3GetObjectResponse = {
#             "Body": StreamingBody(raw_stream=data, content_length=None),
#         }

#         self.__botoClientStubberS3.add_response(
#             method="get_object",
#             service_response=s3GetObjectResponse,
#             expected_params={"Bucket": self.AwsS3BucketName, "Key": self.AwsS3UrlKey},
#         )

#     @patch("botocore.response.StreamingBody.read")
#     @patch("boto3.client")
#     def test_balance_by_file_id_endpoint_status_200(
#         self, mock_boto_3, mock_streaming_body_read
#     ) -> None:

#         mock_boto_3.return_value = self.__botoClientS3

#         with open("csv/transactions_1.csv", "rb") as data:
#             self.mocksS3GetObject(data)
#             mock_streaming_body_read.return_value = data.read()

#         # Arrange
#         form_data = {
#             "client_name": "John Doe",
#             "recipient": "email@fakedomain.net",
#             "subject": "Test email.",
#             "file_id": "transactions_1.csv",
#         }

#         # Act
#         with patch.object(EmailSender, "send_email", new=mock_send_email):
#             response = self.client.post(
#                 "/balance_by_file_id",
#                 data=form_data,
#             )

#         # Assert
#         ## check status code
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
