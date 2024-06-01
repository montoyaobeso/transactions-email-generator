import pandas as pd

from unittest import TestCase

from src.app.transactions.processor import TransactionsProcessor
from src.app.email.content_builder import get_email_body


class TestEmailBodyBuilder(TestCase):

    def test_get_email_body(self):
        # Arrange
        fields = {
            "client_name": "John Doe",
            "total_balance": 100,
            "avg_debit_amount": -100,
            "avg_credit_amount": 100,
            "transactions_per_month": [("July", 2), ("August", 2)],
        }

        # Act
        html_body = get_email_body(**fields)

        # Assert
        self.assertIn("John Doe.", html_body)
        self.assertIn("$100.00", html_body)
        self.assertIn("July: 2", html_body)
        self.assertIn("August: 2", html_body)
