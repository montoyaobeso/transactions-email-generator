from unittest import TestCase

import pandas as pd
import numpy as np
import pandera as pa

from src.app.validator.input_validator import schema


class TestInputValidation(TestCase):

    def test_input_file_correct(self):
        # Arrange
        df = pd.read_csv("csv/transactions_1.csv")

        # Act
        df = schema.validate(df)

        # Assert
        # Check column names
        self.assertIn("Id", df.columns)
        self.assertIn("Date", df.columns)
        self.assertIn("Transaction", df.columns)
        # Check data types
        self.assertEqual(df.Id.dtype, np.dtype("int64"))
        self.assertEqual(df.Date.dtype, np.dtype("datetime64[ns]"))
        self.assertEqual(df.Transaction.dtype, np.dtype("float64"))

    def test_input_file_with_null_values(self):
        # Arrange
        df = pd.read_csv("csv/transactions_with_null_values.csv")

        # Act & Assert
        with self.assertRaises(pa.errors.SchemaErrors):
            df = schema.validate(df, lazy=True)

    def test_input_file_wrong_date(self):
        # Arrange
        df = pd.read_csv("csv/transactions_with_incorrect_date.csv")

        # Act & Assert
        with self.assertRaises(pa.errors.SchemaErrors) as error:
            df = schema.validate(df, lazy=True)
