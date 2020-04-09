import logging
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
        self._user = None
        self._activities = []
        self._content = ""
        self.ckan_api = RemoteCKAN(CKAN_URL, apikey=CKAN_API_KEY)

    def __call__(self):
        self.prepare()
        if self.has_data_for_template():
            self.send()
        else:
            message = f"Failed to prepare notification to user_id = {self.user_id}."
            logging.error(message)

    def prepare(self):
        self._activities = ActivityForUser(self.user_id, self.start_time)()
        if self.has_data_for_template():
            user = {
                "id": self.user_id,
                "email": self.user["email"],
                "name": self.user["display_name"],
            }
            email_template = EmailTemplate(user, self.datasets, self._activities)
            self._content = email_template.html_content()

    def has_data_for_template(self):
        return bool(self.user) and len(self._activities) > 0

    def send(self):
        if self.has_data_for_template():
            email_dispatcher = EmailDispatcher(self.user["email"])
            email_dispatcher(self._content)

    @property
    def datasets(self):
        if not self._datasets:
            ids = [x["object_id"] for x in self._activities]
            self._datasets = CKANMetadata("package_show", ids)()
        return self._datasets

    @property
    def user(self):
        if not self._user:
            result = CKANMetadata("user_show", [self.user_id])()
            if self.user_id in result:
                self._user = result[self.user_id]
        return self._user
