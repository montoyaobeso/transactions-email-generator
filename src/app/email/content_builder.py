from jinja2 import Environment, FileSystemLoader


class EmailBodyBuilder:
    """Class to build a custom HTMP email body."""

    def __init__(
        self,
        client_name,
        total_balance,
        avg_credit_amount,
        avg_debit_amount,
        transactions_history,
    ) -> None:

        self.client_name = client_name
        self.total_balance = total_balance
        self.avg_credit_amount = avg_credit_amount
        self.avg_debit_amount = avg_debit_amount
        self.transactions_history = transactions_history

    def get_email_body(self) -> str:
        """Render HTML email body."""

        file_loader = FileSystemLoader("src/app/templates")

        env = Environment(loader=file_loader)

        template = env.get_template("./email_body.html")

        transactions_summary = []
        for year, txns_per_month in self.transactions_history.items():
            transactions_summary.append(f'<li style="Margin:0">{year}:</li><ul>')
            transactions_summary += (
                "".join(
                    [
                        f'<li style="Margin:0">{month}: {count:,.0f}</li>'
                        for month, count in txns_per_month
                    ]
                ),
            )

            transactions_summary.append("</ul>")

        fields = {
            "client_name": self.client_name.title(),
            "total_balance": f"${self.total_balance:,.2f}",
            "avg_debit_amount": f"${self.avg_debit_amount:,.2f}",
            "avg_credit_amount": f"${self.avg_credit_amount:,.2f}",
            "transactions_history": "".join(transactions_summary),
        }

        return template.render(fields)
