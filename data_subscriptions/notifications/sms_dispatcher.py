import logging
import os
import json
import requests

TWILIO_PASSWORD = os.getenv("TWILIO_PASSWORD")
TWILIO_URL = os.getenv("TWILIO_URL")
FRONTEND_SITE_URL = os.getenv("FRONTEND_SITE_URL")


class SmsDispatcher:
    """
    Dispatch an sms via Twilio.
    """

    def __init__(self, phone):
        self.phone = phone
        self.url = TWILIO_URL + '/send-messages'

    def __call__(self, template_data):
        package_data = template_data['package']
        try:
            body = {
                'message': f"The Dataset {package_data['title']} has been updated, visit the following URL for details: {package_data['url']}",
                'passcode': TWILIO_PASSWORD,
                'recipients': self.phone,
            }
            self.response = requests.post(self.url, json=body)
        except Exception as e:
            logging.error(e.body)
            raise e

        return self.response
