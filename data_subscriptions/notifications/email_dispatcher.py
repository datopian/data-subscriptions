import logging
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Mail, MimeType

API_KEY = os.getenv("SENDGRID_API_KEY")
MAILER_FROM_EMAIL = os.getenv("MAILER_FROM_EMAIL")
MAILER_FROM_NAME = os.getenv("MAILER_FROM_NAME")


class EmailDispatcher:
    def __init__(self, email):
        self.client = SendGridAPIClient(API_KEY)
        self.message = Mail(
            from_email=(MAILER_FROM_EMAIL, MAILER_FROM_NAME),
            to_emails=email,
            subject="Datasets you subscribed were recently changed",
        )

    def __call__(self, content):
        self.message.content = Content(MimeType.html, content)
        try:
            self.response = self.client.send(self.message)
        except Exception as e:
            logging.error(e.body)
            raise e

        was_successful = 200 <= self.response.status_code < 300
        if was_successful:
            logging.info(
                (
                    f"Email notification dispatched to  SendGrid. "
                    f"Status {self.response.status_code}."
                )
            )

        return self.response
