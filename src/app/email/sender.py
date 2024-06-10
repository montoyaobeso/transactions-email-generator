import os

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from src.app.aws.secrets import get_secret


class EmailSender:
    """Class to send emails using SendGrid service."""

    def __init__(self, subject: str, recipient: str, body_content: str) -> None:
        self.subject = subject
        self.recipient = recipient
        self.body_content = body_content

    def set_credentials(self):
        """Set credentials from AWS SecretsManager or Env variables."""

        if "APP_RUNNER_SECRETS" in os.environ:
            secrets = os.environ["APP_RUNNER_SECRETS"]
        else:
            secrets = get_secret(os.environ["SECRET_NAME"])

        os.environ["SENDGRID_SENDER_EMAIL"] = secrets["SENDGRID_SENDER_EMAIL"]
        os.environ["SENDGRID_API_KEY"] = secrets["SENDGRID_API_KEY"]

    def send_email(self) -> None:
        """Send email to recipient."""

        if (
            "SENDGRID_SENDER_EMAIL" not in os.environ
            or "SENDGRID_API_KEY" not in os.environ
        ):
            self.set_credentials()

        sender = os.environ["SENDGRID_SENDER_EMAIL"]
        sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])

        mail = Mail(
            Email(sender),
            To(self.recipient),
            self.subject,
            Content("text/html", self.body_content),
        )

        mail_json = mail.get()

        try:
            sg.client.mail.send.post(request_body=mail_json)
        except Exception as error:
            raise error
