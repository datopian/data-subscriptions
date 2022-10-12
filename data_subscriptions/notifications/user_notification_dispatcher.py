import logging
import os
from operator import itemgetter
from urllib.parse import urljoin

from ckanapi import RemoteCKAN

from data_subscriptions.models import Subscription as Model

from data_subscriptions.notifications.ckan_metadata import CKANMetadata
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.sms_dispatcher import SmsDispatcher
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
                "name": self.user["user_name"],
            }

            email_template = EmailTemplateData(
                user, self.datasets, self.activities)
            self._template_data = email_template.template_data()

    def has_data_for_template(self):
        return bool(self.user) and len(self.activities) > 0

    def send(self):
        if self.has_data_for_template():
            user = self._template_data.get("user", {})
            newDatasetActivites = self.newDatasetMsgFilter(self._template_data)
            datasetUpdateActivities = self.datasetUpdateMsgFilter(
                self._template_data)

            if len(newDatasetActivites) > 0:
                email_dispatcher = EmailDispatcher(self.user["email"])
                email_dispatcher(
                    {"user": user, "package": newDatasetActivites}, "new")

            if len(datasetUpdateActivities) > 0:
                if self.user["phone_number"]:
                    sms_dispatcher = SmsDispatcher(self.user["phone_number"])
                    for package in datasetUpdateActivities:
                        sms_dispatcher(
                            {"user": user, "package": package})
                email_dispatcher = EmailDispatcher(self.user["email"])
                email_dispatcher(
                    {"user": user, "package": datasetUpdateActivities}, "update",
                )

    def newDatasetMsgFilter(self, activitesList):
        return activitesList.get("new_package", [])

    def datasetUpdateMsgFilter(self, activitesList):
        return activitesList.get("packages", [])

    @ property
    def datasets(self):
        if not self._datasets:
            ids = set(map(itemgetter("dataset_id"), self.activities))
            self._datasets = CKANMetadata("package_show", ids)()
        return self._datasets

    @ property
    def user(self):
        if not self._user:
            user_detail = Model.query.filter_by(user_id=self.user_id).first()
            self._user = {
                "user_id": self.user_id,
                "user_name": user_detail.user_name,
                "email": user_detail.email,
                "phone_number": user_detail.phone_number,
            }
        return self._user
