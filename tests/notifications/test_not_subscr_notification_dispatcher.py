import datetime as dt

import pytest

from data_subscriptions.notifications.not_subscribable_notification_dispatcher import (
    NotSubscribableNotifiationDispatcher,
)


def test_send_notification_on_deleted_subscription_by_dataset(
    mocker, db, subscription, ckan_meta_fixture
):
    db.session.add(subscription)
    db.session.commit()
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id

    mocker.patch(
        "data_subscriptions.notifications.not_subscribable_notification_dispatcher.FRONTEND_SITE_URL",
        new="http://localhost/",
    )

    mocker.patch(
        "data_subscriptions.notifications.not_subscribable_notification_dispatcher.CKANMetadata",
        new=ckan_meta_fixture,
    )

    template_data = NotSubscribableNotifiationDispatcher(dataset_id, user_id)
    template_data.template_prepare()

    assert template_data._template_data == {
        "user": {
            "id": "00000000-0000-0000-0000-000000000000",
            "email": "alice@example.com",
            "name": "julietezekwe",
        },
        "non_subs_package": {
            "title": "random-dataset-title",
            "url": "http://localhost/org-1/dataset-1-name",
        },
    }
