import logging
import os
import json
import requests

TWILLIO_PASSWORD = os.getenv("TWILLIO_PASSWORD")
TWILLIO_URL = os.getenv("TWILLIO_URL")


class SmsDispatcher:
    """
    Dispatch an sms via Twilio.
    """

    def __init__(self, phone):
        self.phone = phone
        self.url = TWILLIO_URL + '/send-messages'

    def __call__(self, template_data):
        nl_char = '\n'
        package_data = template_data['package']
        try:
            body = {
                'message': f"The package \"{package_data['title']}\" had the recent changes:\n {nl_char.join(list(map(lambda i: f'- {i}', package_data['activities'])))}",
                'passcode': TWILLIO_PASSWORD,
                'recipients': self.phone,
            }
            self.response = requests.post(self.url, json=body)
        except Exception as e:
            logging.error(e.body)
            raise e

        return self.response
