import os

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from src.app.aws.secrets import get_secret


def set_credentials_from_aws_secrets():
    secret = get_secret("stori-sendgrid")
    os.environ["SENDGRID_SENDER_EMAIL"] = secret["SENDGRID_SENDER_EMAIL"]
    os.environ["SENDGRID_API_KEY"] = secret["SENDGRID_API_KEY"]


def send_email(
    subject: str,
    recipient: str,
    body_content: str,
) -> None:

    if (
        "SENDGRID_SENDER_EMAIL" not in os.environ
        or "SENDGRID_API_KEY" not in os.environ
    ):
        set_credentials_from_aws_secrets()

    sender = os.environ["SENDGRID_SENDER_EMAIL"]
    sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])

    mail = Mail(
        Email(sender),
        To(recipient),
        subject,
        Content("text/html", body_content),
    )

    mail_json = mail.get()

    try:
        sg.client.mail.send.post(request_body=mail_json)
    except Exception as error:
        raise error
