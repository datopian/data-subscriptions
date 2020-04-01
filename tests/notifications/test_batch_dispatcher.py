import datetime as dt

import pytest
from freezegun import freeze_time

from data_subscriptions.notifications.batch_dispatcher import BatchDispatcher


@pytest.fixture(scope="module")
def subject():
    return BatchDispatcher()


@freeze_time("2020-01-01")
def test_call(mocker, subject):
    def users_to_be_notified():
        return [
            ("user-id-1",),
            ("user-id-2",),
        ]

    Dispatcher = mocker.patch(
        "data_subscriptions.notifications.batch_dispatcher.UserNotificationDispatcher"
    )
    mocker.patch.object(subject, "users_to_be_notified", new=users_to_be_notified)
    subject()

    notifications = Dispatcher.call_args_list
    last_notification_time = dt.datetime(2019, 12, 31, 23, 30)
    assert notifications[0].args[0] == "user-id-1"
    assert notifications[0].args[1] == last_notification_time
    assert notifications[1].args[0] == "user-id-2"
    assert notifications[1].args[1] == last_notification_time
