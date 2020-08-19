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
            response = {
                "42": {
                    "object_id": "42",
                    "dataset_id": "42",
                    "title": "random-dataset-title",
                    "name": "dataset-1-name",
                    "id": "42",
                    "organization": {"name": "org-1"},
                },
                "43": {
                    "object_id": "43",
                    "dataset_id": "43",
                    "title": "random-dataset-title",
                    "name": "dataset-2-name",
                    "id": "43",
                    "organization": {"name": "org-2"},
                },
            }
        mock.return_value = response
        return mock

    mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.CKANMetadata",
        new=ckan_metadata,
    )
    return UserNotificationDispatcher("user-id-1", [], dt.datetime(2020, 1, 1))


def test_call(mocker, subject, client, db, subscription_data):
    db.session.add(subscription_data)
    db.session.commit()
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    mocker.patch.object(subject, "activities", [{"object_id": "42"}])
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_called_once()


def test_call_without_activities(mocker, subject, db, subscription_data):
    db.session.add(subscription_data)
    db.session.commit()
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_not_called()


def test_call_without_user(mocker, subject, db, subscription_data):
    db.session.add(subscription_data)
    db.session.commit()
    mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.CKANMetadata",
    )
    subject = UserNotificationDispatcher("user-id-1", [], dt.datetime(2020, 1, 1))
    mocker.patch.object(subject, "prepare")
    mocker.patch.object(subject, "send")
    subject()
    subject.prepare.assert_called_once()
    subject.send.assert_not_called()


def test_prepare_tempate_new_dataset_notification(
    mocker, subject, db, subscription_data
):
    db.session.add(subscription_data)
    db.session.commit()

    activities = [
        {
            "dataset_id": "42",
            "activity": {
                "object_id": "42",
                "id": "",
                "data": {"body": {}},
                "activity_type": "new package",
            },
        }
    ]

    subject = UserNotificationDispatcher(
        "user-id-1", activities, dt.datetime(2020, 1, 1)
    )
    subject.prepare()
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.send()
    assert len(subject.newDatasetMsgFilter(subject._template_data)) == 1
    dispatcher.return_value.assert_called_once()


def test_prepare_tempate_dataset_update_notification(
    mocker, subject, db, subscription_data
):
    db.session.add(subscription_data)
    db.session.commit()

    activities = [
        {
            "dataset_id": "43",
            "activity": {
                "object_id": "43",
                "id": "",
                "data": {"body": {}},
                "activity_type": "changed package",
            },
        }
    ]

    subject = UserNotificationDispatcher(
        "user-id-1", activities, dt.datetime(2020, 1, 1)
    )
    subject.prepare()
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.send()
    print(subject._template_data)
    assert len(subject.datasetUpdateMsgFilter(subject._template_data)) == 1
    dispatcher.return_value.assert_called_once()


def test_send_when_both_new_dataset_and_update_msg_on_activity_list(
    mocker, subject, db, subscription_data
):
    db.session.add(subscription_data)
    db.session.commit()

    activities = [
        {
            "dataset_id": "42",
            "activity": {
                "object_id": "42",
                "id": "",
                "data": {"body": {}},
                "activity_type": "new package",
            },
        },
        {
            "dataset_id": "43",
            "activity": {
                "object_id": "43",
                "id": "",
                "data": {"body": {}},
                "activity_type": "changed package",
            },
        },
    ]

    subject = UserNotificationDispatcher(
        "user-id-1", activities, dt.datetime(2020, 1, 1)
    )
    subject.prepare()
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.send()
    assert len(subject.datasetUpdateMsgFilter(subject._template_data)) == 1
    assert len(subject.datasetUpdateMsgFilter(subject._template_data)) == 1
    assert dispatcher.call_count == 2


def test_dont_dispatch_nofication_when_there_are_others_activity(
    mocker, subject, db, subscription_data
):
    db.session.add(subscription_data)
    db.session.commit()

    activities = [
        {
            "dataset_id": "43",
            "activity": {
                "object_id": "43",
                "id": "",
                "data": {"body": {}},
                "activity_type": "new packageextra",
            },
        }
    ]

    subject = UserNotificationDispatcher(
        "user-id-1", activities, dt.datetime(2020, 1, 1)
    )
    subject.prepare()
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.send()
    assert len(subject.datasetUpdateMsgFilter(subject._template_data)) == 0
    dispatcher.return_value.assert_not_called()


def test_prepare(mocker, subject, db, subscription_data):
    db.session.add(subscription_data)
    db.session.commit()
    subject.activities = [
        {"dataset_id": "1", "activity": {"object_id": "1"}},
        {"dataset_id": "1", "activity": {"object_id": "1"}},
    ]
    template = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailTemplateData"
    )
    subject.prepare()

    assert subject._template_data == template.return_value.template_data.return_value


def test_send_without_activities(mocker, subject, db, subscription_data):
    db.session.add(subscription_data)
    db.session.commit()
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    subject.send()
    dispatcher.return_value.assert_not_called()


def test_send_with_activities(mocker, subject, db, subscription_data):
    db.session.add(subscription_data)
    db.session.commit()
    dispatcher = mocker.patch(
        "data_subscriptions.notifications.user_notification_dispatcher.EmailDispatcher"
    )
    mocker.patch.object(subject, "activities", [{"dataset-1": {"id": "1"}}])
    mocker.patch.object(
        subject,
        "_template_data",
        {"packages": [{"title": "", "url": "", "activities": []}], "new_package": []},
    )
    subject.send()
    dispatcher.return_value.assert_called_once()
