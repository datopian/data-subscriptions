import os

from ckanapi import RemoteCKAN

from data_subscriptions.worker.activity_for_user import ActivityForUser
from data_subscriptions.notifications.ckan_metadata import CKANMetadata
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.email_template import EmailTemplate


CKAN_URL = os.getenv("CKAN_URL")
CKAN_API_KEY = os.getenv("CKAN_API_KEY")


class UserNotificationDispatcher:
    def __init__(self, user_id, time_of_last_notification):
        self.user_id = user_id
        self.start_time = time_of_last_notification
        self._datasets = None
        self._email_and_name = None
        self.ckan_api = RemoteCKAN(CKAN_URL, apikey=CKAN_API_KEY)

    def __call__(self):
        self.prepare()
        self.send()

    def prepare(self):
        self.activities = ActivityForUser(self.user_id, self.start_time)()
        user = {
            "id": self.user_id,
            "email": self.email_and_name[0],
            "name": self.email_and_name[1],
        }
        email_template = EmailTemplate(user, self.datasets, self.activities)
        self.content = email_template.html_content()

    def send(self):
        if len(self.activities) > 0:
            email_dispatcher = EmailDispatcher(self.email_and_name)
            email_dispatcher(self.content)

    @property
    def datasets(self):
        if not self._datasets:
            ids = [x["object_id"] for x in self.activities]
            self._datasets = CKANMetadata("package_show", ids)()
        return self._datasets

    @property
    def email_and_name(self):
        if not self._email_and_name:
            user = CKANMetadata("user_show", [self.user_id])()[self.user_id]
            self._email_and_name = user["email"], user["display_name"]
        return self._email_and_name
