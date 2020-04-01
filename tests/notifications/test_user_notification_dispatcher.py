import datetime as dt

import pytest

from data_subscriptions.notifications.user_notification_dispatcher import (
    UserNotificationDispatcher,
)


@pytest.fixture(scope="module")
def subject():
    return UserNotificationDispatcher("user-id-1", dt.datetime(2020, 1, 1))


def test_call(mocker, subject):
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_called_once()


def test_prepare(mocker, subject):
    activities = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.ActivityForUser"
    )
    api = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.RemoteCKAN"
    )
    template = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailTemplate"
    )
    subject.prepare()

    assert subject.activities == activities.return_value.return_value
    assert subject.content == template.return_value.html_content.return_value
    activities.assert_called_once_with(subject.user_id, subject.start_time)


def test_send_without_activities(mocker, subject):
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.activities = []
    subject.send()
    dispatcher.return_value.assert_not_called()


def test_send_with_activities(mocker, subject):
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.activities = [{"object_id": "xyz"}]
    subject.content = "<html></html>"
    subject.send()
    dispatcher.return_value.assert_called_once_with(subject.content)
