import datetime as dt

import pytest

from data_subscriptions.notifications.not_subscribable_notification_dispatcher import (
    NotSubscribableNotifiationDispatcher,
)


def test_send_notification_on_deleted_subscription_by_dataset(
    mocker, ckan_meta_fixture
):
    template_data = NotSubscribableNotifiationDispatcher(
        "b72159fe-67d8-4ea7-8313-af2bf9210799", "user1"
    )
    mocker.patch(
        "data_subscriptions.notifications.not_subscribable_notification_dispatcher.FRONTEND_SITE_URL",
        new="http://localhost/",
    )

    mocker.patch(
        "data_subscriptions.notifications.not_subscribable_notification_dispatcher.CKANMetadata",
        new=ckan_meta_fixture,
    )

    template_data.template_prepare()
    assert template_data._template_data == {
        "user": {"id": "user1", "email": "user1@gmail.com", "name": "nouser"},
        "non_subs_package": {
            "title": "random-dataset-title",
            "url": "http://localhost/org-1/dataset-1-name",
        },
    }
