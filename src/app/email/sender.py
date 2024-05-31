import os

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


def send_email(
    subject: str,
    sender: str,
    recipient: str,
    body_content: str,
) -> None:

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
