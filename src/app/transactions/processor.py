import calendar

import pandas as pd
from datetime import date


class TransactionsProcessor:
    def __init__(self, transactions: pd.DataFrame) -> None:
        self.txns = transactions

    def get_balance(self):
        """Return account balance given all transactions.

        Returns:
            int: account balance.
        """
        return self.txns["value"].sum()

    def get_avg_debit_amount(self):
        """Return average debit amount.

        Returns:
            int: average debit amount.
        """
        return self.txns[self.txns["value"] < 0]["value"].mean()

    def get_avg_credit_amount(self):
        """Return average credit amount.

        Returns:
            int: average credit amount.
        """
        return self.txns[self.txns["value"] >= 0]["value"].mean()

    def get_transactions_history(self) -> list:
        """Return a sorted list of transactions per month and year

        Returns:
            list: sorted list of tuples with transactions per month.
        """
        df = self.txns.copy()

        df["date"] = pd.to_datetime(df["date"])

        df["month"] = df["date"].dt.strftime("%B")
        df["year"] = df["date"].dt.strftime("%Y")

        grouped_transactions = df.groupby(["year", "month"]).size().to_dict()

        txns_by_year = {}
        for t, count in grouped_transactions.items():
            year, month = t
            if year in txns_by_year.keys():
                txns_by_year[year].append({month: count})
            else:
                txns_by_year[year] = [{month: count}]

        months = [month.lower() for month in calendar.month_name if month]

        for year, count_per_month in txns_by_year.items():
            # Convert list of dicts to dict
            count_per_month = dict((key, d[key]) for d in count_per_month for key in d)

            # Sort by month
            ordered = sorted(
                count_per_month.keys(),
                key=lambda m: months.index(m.lower()),
            )

            # Build the list with counting per month
            txns_by_year[year] = [
                (month.title(), count_per_month[month.title()]) for month in ordered
            ]

        return txns_by_year
