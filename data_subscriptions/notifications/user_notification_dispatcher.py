import os

from ckanapi import RemoteCKAN

from data_subscriptions.worker.activity_for_user import ActivityForUser
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.email_template import EmailTemplate


CKAN_URL = os.getenv("CKAN_URL")
CKAN_API_KEY = os.getenv("CKAN_API_KEY")


class UserNotificationDispatcher:
    def __init__(self, user_id, time_of_last_notification):
        self.user_id = user_id
        self.start_time = time_of_last_notification

    def __call__(self):
        self.prepare()
        self.send()

    def prepare(self):
        self.activities = ActivityForUser(self.user_id, self.start_time)()
        email_template = EmailTemplate(self.user_id, self.activities)
        self.content = email_template.html_content()

    def send(self):
        if len(self.activities) > 0:
            email_dispatcher = EmailDispatcher(self.email_and_name())
            email_dispatcher(self.content)

    def email_and_name(self):
        api = RemoteCKAN(CKAN_URL, apikey=CKAN_API_KEY)
        user = api.action.user_show(id=self.user_id)
        return user["email"], user["name"]
