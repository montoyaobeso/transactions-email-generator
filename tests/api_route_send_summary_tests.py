from unittest import TestCase
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

import src.app.email.sender as sender
from src.app.main import app


def new_send_email(cls, *args, **kwargs):
    return None


class UploadTest(TestCase):
    client = TestClient(app)

    def test_send_summary_endpoint_status_200(self):

        # Arrange
        with open("csv/transactions_1.csv", "rb") as f:
            filebody = f.read()

        form_data = {
            "client_name": "John Doe",
            "recipient": "email@fakedomain.net",
            "subject": "Test email.",
        }

        # Act
        with patch.object(sender, "send_email", new=new_send_email):
            response = self.client.post(
                "/send_summary",
                data=form_data,
                files={
                    "file": ("transactions_1.csv", filebody),
                },
            )

        # Assert
        ## check status code
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_send_summary_status_400(self):
        # Arrange
        with open("csv/transactions_with_null_values.csv", "rb") as f:
            filebody = f.read()

        form_data = {
            "client_name": "John Doe",
            "recipient": "email@fakedomain.net",
            "subject": "Test email.",
        }

        # Act
        response = self.client.post(
            "/send_summary",
            data=form_data,
            files={
                "file": ("transactions_with_null_values.csv", filebody),
            },
        )

        # Assert
        ## check status code
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_send_summary_status_400_not_csv_file(self):
        # Arrange
        with open("csv/transactions.txt", "rb") as f:
            filebody = f.read()

        form_data = {
            "client_name": "John Doe",
            "recipient": "email@fakedomain.net",
            "subject": "Test email.",
        }

        expected_content = b'{"message":"Only CSV files are supported, you provided transactions.txt."}'

        # Act
        response = self.client.post(
            "/send_summary",
            data=form_data,
            files={
                "file": ("transactions.txt", filebody),
            },
        )

        # Assert
        ## check status code
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(response.content, expected_content)
