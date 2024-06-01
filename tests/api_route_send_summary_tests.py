import io
from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from src.app.main import app

from unittest.mock import patch


from mock import patch


class UploadTest(TestCase):
    client = TestClient(app)

    @patch("src.app.email.content_builder.get_email_body")
    @patch("src.app.email.sender.send_email")
    def test_send_summary_endpoint_status_200(
        self,
        get_email_body_mock,
        send_email_mock,
    ):

        # Mocks
        get_email_body_mock.return_value = None
        send_email_mock.return_value = None

        # Arrange
        with open("csv/transactions_1.csv", "rb") as f:
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
                "file": ("transactions_1.csv", filebody),
            },
        )

        # Assert
        ## check status code
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch("src.app.email.content_builder.get_email_body")
    @patch("src.app.email.sender.send_email")
    def test_send_summary_status_400(
        self,
        get_email_body_mock,
        send_email_mock,
    ):

        # Mocks
        get_email_body_mock.return_value = None
        send_email_mock.return_value = None

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

    @patch("src.app.email.content_builder.get_email_body")
    @patch("src.app.email.sender.send_email")
    def test_send_summary_status_400_not_csv_file(
        self,
        get_email_body_mock,
        send_email_mock,
    ):

        # Mocks
        get_email_body_mock.return_value = None
        send_email_mock.return_value = None

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
