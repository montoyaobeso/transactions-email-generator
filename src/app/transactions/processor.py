import calendar

import pandas as pd


class TransactionsProcessor:
    def __init__(self, transactions: pd.DataFrame) -> None:
        self.txns = transactions

    def get_balance(self):
        """Return account balance given all transactions.

        Returns:
            int: account balance.
        """
        return self.txns["Transaction"].sum()

    def get_avg_debit_amount(self):
        """Return average debit amount.

        Returns:
            int: average debit amount.
        """
        return self.txns[self.txns["Transaction"] < 0]["Transaction"].mean()

    def get_avg_credit_amount(self):
        """Return average credit amount.

        Returns:
            int: average credit amount.
        """
        return self.txns[self.txns["Transaction"] >= 0]["Transaction"].mean()

    def get_montly_transactions(self) -> list:
        """Return a sorted list of transactions per month

        Returns:
            list: sorted list of tuples with transactions per month.
        """
        df = self.txns.copy()
        df["Month"] = df["Date"].dt.strftime("%B")

        transactions = df.groupby(["Month"]).size().to_dict()

        months = [month.lower() for month in calendar.month_name if month]

        ordered = sorted(
            list(transactions.keys()), key=lambda m: months.index(m.lower())
        )

        return [(month.title(), transactions[month.title()]) for month in ordered]
