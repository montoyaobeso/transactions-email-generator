from jinja2 import Environment, FileSystemLoader


class EmailBodyBuilder:

    def __init__(
        self,
        client_name,
        total_balance,
        avg_credit_amount,
        avg_debit_amount,
        transactions_per_month,
    ) -> None:

        self.client_name = client_name
        self.total_balance = total_balance
        self.avg_credit_amount = avg_credit_amount
        self.avg_debit_amount = avg_debit_amount
        self.transactions_per_month = transactions_per_month

    def get_email_body(self) -> str:

        file_loader = FileSystemLoader("src/app/templates")

        env = Environment(loader=file_loader)

        template = env.get_template("./email_body.html")

        fields = {
            "client_name": self.client_name.title(),
            "total_balance": f"${self.total_balance:,.2f}",
            "avg_debit_amount": f"${self.avg_debit_amount:,.2f}",
            "avg_credit_amount": f"${self.avg_credit_amount:,.2f}",
            "transactions_per_month": "".join(
                [
                    f'<li style="Margin:0">{month}: {count:,.0f}</li>'
                    for month, count in self.transactions_per_month
                ]
            ),
        }

        return template.render(fields)
