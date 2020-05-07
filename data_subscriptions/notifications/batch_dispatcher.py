import datetime as dt
import os

from data_subscriptions.extensions import db
from data_subscriptions.notifications.email_dispatcher import EmailDispatcher
from data_subscriptions.notifications.user_notification_dispatcher import (
    UserNotificationDispatcher,
)

NOTIFICATION_FREQUENCY = int(
    os.getenv("TIME_IN_SECONDS_BETWEEN_NOTIFICATION_DELIVERIES")
)

QUERY = """
SELECT
	DISTINCT(subscription.user_id)
FROM
	dataset_activity_list,
	json_array_elements(dataset_activity_list.blob) AS activity
JOIN
	subscription ON dataset_id = subscription.dataset_id
WHERE
	(activity->>'timestamp')::timestamptz > :start_time;
"""


class BatchDispatcher:
    """
    Dispatch a notification for each user requiring one at this moment.
    """

    def __call__(self):
        users = self.users_to_be_notified()
        for row in users:
            user_notification = UserNotificationDispatcher(
                row[0], self.last_notification_time()
            )
            user_notification()

    def users_to_be_notified(self):
        return db.session.execute(QUERY, {"start_time": self.last_notification_time()})

    def last_notification_time(self):
        return dt.datetime.now() - dt.timedelta(seconds=NOTIFICATION_FREQUENCY)
