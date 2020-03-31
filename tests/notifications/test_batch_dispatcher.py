import datetime as dt

import pytest

from data_subscriptions.notifications.batch_dispatcher import BatchDispatcher


@pytest.fixture(scope="module")
def subject():
    return BatchDispatcher()


def test_call(mocker, subject):
    users = [
        ("user-id-1",),
        ("user-id-2",),
    ]
    Dispatcher = mocker.patch(
        "data_subscriptions.notifications.batch_dispatcher.UserNotificationDispatcher"
    )
    mocker.patch.object(subject, "users_to_be_notified", new=lambda: users)
    subject()
    assert Dispatcher.call_args_list[0].args[0] == users[0][0]
    assert Dispatcher.call_args_list[1].args[0] == users[1][0]
