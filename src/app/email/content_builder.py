from jinja2 import Environment, FileSystemLoader


def get_email_body(
    client_name: str,
    total_balance: float,
    avg_debit_amount: float,
    avg_credit_amount: float,
    transactions_per_month: list,
) -> str:

    file_loader = FileSystemLoader("src/app/templates")

    env = Environment(loader=file_loader)

    template = env.get_template("./email_body.html")

    fields = {
        "client_name": client_name.title(),
        "total_balance": f"${total_balance:,.2f}",
        "avg_debit_amount": f"${avg_debit_amount:,.2f}",
        "avg_credit_amount": f"${avg_credit_amount:,.2f}",
        "transactions_per_month": "".join(
            [
                f'<li style="Margin:0">{month}: {count:,.0f}</li>'
                for month, count in transactions_per_month
            ]
        ),
    }

    return template.render(fields)
