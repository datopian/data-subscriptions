import datetime as dt

import pytest

from data_subscriptions.notifications.user_notification_dispatcher import (
    UserNotificationDispatcher,
)


@pytest.fixture
def subject(mocker):
    def ckan_metadata(action, *args, **kwargs):
        mock = mocker.MagicMock(name="ckan_metadata")
        if action == "package_show":
            response = {"42": {"object_id": "42"}}
        elif action == "user_show":
            response = {
                "user-id-1": {"email": "alice@example.com", "display_name": "Alice"}
            }
        mock.return_value = response
        return mock

    mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.CKANMetadata",
        new=ckan_metadata,
    )
    return UserNotificationDispatcher("user-id-1", dt.datetime(2020, 1, 1))


def test_call(mocker, subject):
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    mocker.patch.object(subject, "_activities", [{"object_id": "42"}])
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_called_once()


def test_call_without_activities(mocker, subject):
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_not_called()


def test_call_without_user(mocker, subject):
    mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.CKANMetadata",
    )
    subject = UserNotificationDispatcher("user-id-1", dt.datetime(2020, 1, 1))
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_not_called()


def test_prepare(mocker, subject):
    activities = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.ActivityForUser"
    )
    activities.return_value.return_value = [
        {"object_id": "1"},
        {"object_id": "1"},
    ]
    template = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailTemplate"
    )
    subject.prepare()

    assert subject._activities == activities.return_value.return_value
    assert subject._content == template.return_value.html_content.return_value
    activities.assert_called_once_with(subject.user_id, subject.start_time)


def test_send_without_activities(mocker, subject):
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.send()
    dispatcher.return_value.assert_not_called()


def test_send_with_activities(mocker, subject):
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    mocker.patch.object(subject, "_activities", [{"dataset-1": {"id": "1"}}])
    mocker.patch.object(subject, "_content", "<html></html>")
    subject.send()
    dispatcher.return_value.assert_called_once_with(subject._content)