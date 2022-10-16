import datetime as dt
import os

from data_subscriptions.extensions import db
from data_subscriptions.notifications.activity_groups import ActivityList
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.user_notification_dispatcher import (
    UserNotificationDispatcher,
)

NOTIFICATION_FREQUENCY = int(
    os.getenv("TIME_IN_SECONDS_BETWEEN_NOTIFICATION_DELIVERIES")
)


class BatchDispatcher:
    """
    Dispatch a notification for each user requiring one at this moment.
    """

    def __call__(self):
        start_time = self.last_notification_time()
        activities_by_user = ActivityList(start_time).by_user()
        for user_id, xs in activities_by_user:
            activities = [x for x in xs]
            dispatcher = UserNotificationDispatcher(
                user_id, activities, start_time)
            dispatcher()

    def last_notification_time(self):
        return dt.datetime.now() - dt.timedelta(seconds=NOTIFICATION_FREQUENCY)
