import pandas as pd

from unittest import TestCase

from src.app.transactions.processor import TransactionsProcessor
from src.app.validator.input_validator import schema


class TestTransactionsProcessor(TestCase):

    def test_transactions_processor(self):
        # Arrange
        df = schema.validate(pd.read_csv("csv/transactions_1.csv"))

        expected_total_balance = 39.74
        expected_avg_credit_amount = 35.25
        expected_avg_debit_amount = -15.38
        expected_transactions_per_month = [("July", 2), ("August", 2)]

        # Act
        tp = TransactionsProcessor(transactions=df)

        # Assert
        self.assertTrue(tp.get_balance() == expected_total_balance)
        self.assertTrue(tp.get_avg_credit_amount() == expected_avg_credit_amount)
        self.assertTrue(tp.get_avg_debit_amount() == expected_avg_debit_amount)
        self.assertTrue(tp.get_montly_transactions() == expected_transactions_per_month)
