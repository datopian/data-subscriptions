import logging
import os
from operator import itemgetter
from urllib.parse import urljoin

from data_subscriptions.models import Subscription as Model
from data_subscriptions.notifications.ckan_metadata import CKANMetadata
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.email_template import EmailTemplateData

FRONTEND_SITE_URL = os.getenv("FRONTEND_SITE_URL")


class NotSubscribableNotifiationDispatcher:
    """
    Dispatch email notification to subscriber when a subscription was deleted.
    """

    def __init__(self, dataset_id, user_id):
        self.dataset_id = dataset_id
        self.user_id = user_id

        self._dataset = None
        self._user = None
        self._template_data = {}

    def __call__(self):
        if self.dataset and self.user:
            self.template_prepare()
            self.send()

    def template_prepare(self):
        user = {
            "id": self.user_id,
            "email": self.user["email"],
            "name": self.user["user_name"],
        }

        pkg_url = urljoin(FRONTEND_SITE_URL, self.dataset["organization"]["name"])
        dataset_meta = {
            "title": self.dataset["title"],
            "url": "%s/%s" % (pkg_url, self.dataset["name"]),
        }
        self._template_data.update({"user": user})
        self._template_data.update({"non_subs_package": dataset_meta})

    def send(self):
        email_dispatcher = EmailDispatcher(self.user["email"])
        email_dispatcher(self._template_data)

    @property
    def dataset(self):
        if not self._dataset:
            result = CKANMetadata("package_show", [self.dataset_id])()
            if self.dataset_id in result:
                self._dataset = result[self.dataset_id]
        return self._dataset

    @property
    def user(self):
        if not self._user:
            user_detail = Model.query.filter_by(user_id=self.user_id).first()
            self._user = {
                "user_id": self.user_id,
                "user_name": user_detail.user_name,
                "email": user_detail.email,
            }
        return self._user
