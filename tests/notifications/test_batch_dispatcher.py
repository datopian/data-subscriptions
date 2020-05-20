import datetime as dt

import pytest
from freezegun import freeze_time

from data_subscriptions.notifications.batch_dispatcher import BatchDispatcher


@pytest.fixture(scope="module")
def subject():
    return BatchDispatcher()


@freeze_time("2020-01-01")
def test_call(mocker, subject):
    activity_list = mocker.patch(
        "data_subscriptions.notifications.batch_dispatcher.ActivityList"
    )
    activity_list.return_value.by_user.return_value = [
        ["user-id-1", ["x", "y"]],
        ["user-id-2", ["z"]],
    ]

    Dispatcher = mocker.patch(
        "data_subscriptions.notifications.batch_dispatcher.UserNotificationDispatcher"
    )
    subject()

    notifications = Dispatcher.call_args_list
    last_notification_time = dt.datetime(2019, 12, 31, 23, 30)
    assert notifications[0].args[0] == "user-id-1"
    assert notifications[0].args[1] == ["x", "y"]
    assert notifications[0].args[2] == last_notification_time
    assert notifications[1].args[0] == "user-id-2"
    assert notifications[1].args[1] == ["z"]
    assert notifications[1].args[2] == last_notification_time
