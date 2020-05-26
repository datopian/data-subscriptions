import logging
import os
from operator import itemgetter
from urllib.parse import urljoin

from ckanapi import RemoteCKAN

from data_subscriptions.notifications.ckan_metadata import CKANMetadata
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.email_template import EmailTemplateData

FRONTEND_SITE_URL = os.getenv("FRONTEND_SITE_URL")


class UserNotificationDispatcher:
    """
    Collect information for a user notification and dispatch it.
    """

    def __init__(self, user_id, activities, time_of_last_notification):
        self.user_id = user_id
        self.activities = activities
        self.start_time = time_of_last_notification

        self._datasets = None
        self._user = None
        self._template_data = None

    def __call__(self):
        self.prepare()
        if self.has_data_for_template():
            self.send()
        else:
            message = f"Failed to prepare notification to user_id = {self.user_id}."
            logging.error(message)

    def prepare(self):
        if self.has_data_for_template():
            user = {
                "id": self.user_id,
                "email": self.user["email"],
                "name": self.user["display_name"],
            }

            email_template = EmailTemplateData(user, self.datasets, self.activities)
            self._template_data = email_template.template_data()

    def has_data_for_template(self):
        return bool(self.user) and len(self.activities) > 0

    def send(self):
        if self.has_data_for_template():
            email_dispatcher = EmailDispatcher(self.user["email"])
            email_dispatcher(self._template_data)

    @property
    def datasets(self):
        if not self._datasets:
            ids = set(map(itemgetter("dataset_id"), self.activities))
            self._datasets = CKANMetadata("package_show", ids)()
        return self._datasets

    @property
    def user(self):
        if not self._user:
            result = CKANMetadata("user_show", [self.user_id])()
            if self.user_id in result:
                self._user = result[self.user_id]
        return self._user
