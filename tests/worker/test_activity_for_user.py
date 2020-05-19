import datetime as dt

from data_subscriptions.models import DatasetActivityList
from data_subscriptions.worker.activity_for_user import ActivityForUser


def test_call_for_user_without_subscriptions(db, dataset_activity_list):
    db.session.add(dataset_activity_list)
    db.session.commit()
    subject = ActivityForUser("a-new-user", dt.datetime(2020, 1, 1))
    assert subject() == []


def test_call_for_user_with_subscriptions(db, dataset_activity_list, subscription):
    db.session.add(dataset_activity_list)
    db.session.add(subscription)
    db.session.commit()
    subject = ActivityForUser(subscription.user_id, dt.datetime(2020, 1, 1))
    assert subject() == [
        {
            "object_id": subscription.dataset_id,
            "timestamp": "2020-02-01T00:00:00.000000",
        }
    ]


def test_call_for_user_with_subscriptions_but_no_activity(db, subscription):
    db.session.add(subscription)
    db.session.commit()
    subject = ActivityForUser(subscription.user_id, dt.datetime(2020, 1, 1))
    assert subject() == []


def test_call_for_user_with_subscriptions_but_no_activity_since_start_time(
    db, dataset_activity_list, subscription
):
    db.session.add(dataset_activity_list)
    db.session.add(subscription)
    db.session.commit()
    subject = ActivityForUser(subscription.user_id, dt.datetime(2020, 2, 1))
    assert subject() == []


def test_call_for_user_with_subscriptions_and_part_of_activity_since_start_time(
    db, dataset_activity_list, subscription
):
    new_activity = [
        {
            "object_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "timestamp": "2020-02-01T00:00:01.000000",
        }
    ]
    db.session.add(
        DatasetActivityList(
            blob=new_activity,
            collected_at=dataset_activity_list.collected_at,
            last_activity_created_at=dt.datetime(2020, 2, 1, 0, 0, 1),
        )
    )
    db.session.add(dataset_activity_list)
    db.session.add(subscription)
    db.session.commit()
    subject = ActivityForUser(subscription.user_id, dt.datetime(2020, 2, 1))
    assert subject() == new_activity


def test_call_for_user_with_subscriptions_with_multiple_datasets_in_db(
    db, dataset_activity_list, subscription
):
    activity_for_another_dataset = [
        {
            "object_id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
            "timestamp": "2020-02-01T00:00:00.000000",
        }
    ]
    db.session.add(
        DatasetActivityList(
            blob=activity_for_another_dataset,
            collected_at=dataset_activity_list.collected_at,
            last_activity_created_at=dt.datetime(2020, 2, 1, 0, 0, 1),
        )
    )
    db.session.add(dataset_activity_list)
    db.session.add(subscription)
    db.session.commit()
    subject = ActivityForUser(subscription.user_id, dt.datetime(2020, 1, 1))
    results = subject()
    assert len(results) == 1
    assert results[0]["object_id"] == subscription.dataset_id
